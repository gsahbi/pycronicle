import time
import json
import inspect


def now_msec():
    return int(time.time() * 1000)


def cexit(ret=0, e=None):
    m = {"complete": 1}
    if ret != 0:
        m["code"] = ret
        m["description"] = "Job failed with " + str(e) if e else "No failure desription"
    print(json.dumps(m))
    exit(ret)


def cprogress(progress):
    m = {"progress": progress}
    print(json.dumps(m))


def ctable(table):
    m = {"table": table}
    print(json.dumps(m))


def cperf(**kwargs):
    m = {"perf": {'scale': 1000, **kwargs}}
    print(json.dumps(m))


def cprofile(f):
    def wrap(*args, **kwargs):
        spec = inspect.getfullargspec(f).args
        if spec and spec[0] == 'self':
            fn = args[0].__class__.__name__
        else:
            fn = f.__name__
        started_at = now_msec()
        result = f(*args, **kwargs)
        cperf(**{fn: now_msec() - started_at})
        return result
    return wrap


def cprofile_named(fname=None):
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            fn = f.__name__ if fname is None else fname
            started_at = now_msec()
            result = f(*args, **kwargs)
            cperf(**{fn: now_msec() - started_at})
            return result
        return wrapped_f
    return wrap
