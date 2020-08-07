import time
import json


def cexit(ret=0, e=None):
    m = {"complete": 1}
    if ret != 0:
        m["code"] = ret
        m["message"] = "Job failed with " + str(e) if e else "No failure desription"
    print(json.dumps(m))
    exit(ret)


def cprogress(progress):
    m = {"progress": progress}
    print(json.dumps(m))


def cperf(**kwargs):
    m = {"perf": kwargs}
    print(json.dumps(m))


def now_msec():
    return int(time.time() * 1000)


def cprofile(func):
    def wrap(*args, **kwargs):
        started_at = now_msec()
        result = func(*args, **kwargs)
        cperf(**{'scale': 1000, func.__name__: now_msec() - started_at})
        return result

    return wrap
