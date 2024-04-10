from time import time, perf_counter, time_ns, perf_counter_ns

def SecondsToMilliseconds(sec: float) -> float: return sec * 1000.0
def MillisecondsToSeconds(ms : float) -> float: return ms  / 1000.0

def SecondsToNenoseconds(sec: float) -> float: return sec * (10**9)
def NenosecondsToSeconds(ns : float) -> float: return ns  / (10**9)
