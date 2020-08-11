import time
import json
import inspect

__perf__ = {}

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


def cperf():
    m = {"perf": {'scale': 1000, **__perf__}}
    print(json.dumps(m))


def cperf_add(**kwargs):
    for k, v in kwargs.items():
        if k not in __perf__:
            __perf__[k] = 0
        __perf__[k] = __perf__[k] + v

def cprofile(f):
    def wrap(*args, **kwargs):
        global __perf__
        spec = inspect.getfullargspec(f).args
        if spec and spec[0] == 'self':
            fn = args[0].__class__.__name__
        else:
            fn = f.__name__
        started_at = now_msec()
        result = f(*args, **kwargs)
        if fn not in __perf__:
            __perf__[fn] = 0
        __perf__[fn] = __perf__[fn] + now_msec() - started_at
        return result
    return wrap


def cprofile_named(fname=None):
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            global __perf__
            fn = f.__name__ if fname is None else fname
            started_at = now_msec()
            result = f(*args, **kwargs)
            if fn not in __perf__:
                __perf__[fn] = 0
            __perf__[fn] = __perf__[fn] + now_msec() - started_at
            return result
        return wrapped_f
    return wrap
