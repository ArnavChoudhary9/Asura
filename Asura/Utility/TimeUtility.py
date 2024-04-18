from time import time, perf_counter, time_ns, perf_counter_ns, sleep

class TimeConverter:
    class Unit:
        Second      : float = 10**0
        MilliSecond : float = 10**-3
        MicroSecond : float = 10**-6
        NenoSecond  : float = 10**-9

    @classmethod
    def Convert(cls, value: float, fromUnit: float, toUnit: float) -> float:
        # This is direct operation that will be done if we do:
        #   valueInSecond = Convert(value, fromUnit, Unit.Second)
        #   finalValue = Convert(value, Unit.Second, toUnit)
        return value * fromUnit / toUnit

def Wait(seconds: float) -> None: sleep(seconds)
