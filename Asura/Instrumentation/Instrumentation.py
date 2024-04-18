from ..Utility import perf_counter_ns, TimeConverter, TextIO, DataClass

from multiprocessing import current_process
from threading import current_thread
from json import dump as JSONDump

@DataClass
# Just a container for profile results
class ProfileResult:
    Name: str

    Start: float = 0.0
    End: float = 0.0
    PID: int = 0
    TID: int = 0

    Complete: bool = False

class Instrumentor:
    __CurrentSession: str
    __OutputStream: TextIO
    __ProfileCount: int

    def __init__(self) -> None:
        self.__CurrentSession = ""
        self.__ProfileCount = 0

    def BeginSession(self, name: str) -> None:
        self.__CurrentSession = name
        self.__OutputStream = open("{}.json".format(name), "w")
        self.WriteHeader()

    def EndSession(self) -> None:
        self.WriteFooter()
        self.__OutputStream.close()
        self.__CurrentSession = ""
        self.__ProfileCount = 0

    def WriteHeader(self) -> None:
        self.__OutputStream.write("{\"otherData\": {}, \"displayTimeUnit\": \"ms\", \"traceEvents\": [ ")

    def WriteFooter(self) -> None:
        self.__OutputStream.write("]}")
        self.__OutputStream.flush()
    
    def WriteProfile(self, result: ProfileResult) -> None:
        if (self.__ProfileCount > 0): self.__OutputStream.write(", ")
        self.__ProfileCount += 1

        JSONDump(
            {
                "name" : result.Name,
                "cat"  : "Function",
                "ph"   : "X",
                "pid"  : result.PID,
                "tid"  : result.TID,
                "dur"  : result.End - result.Start,
                "ts"   : result.Start
            },
            self.__OutputStream
        )

    def WriteEvent(self, event) -> None:
        if (self.__ProfileCount > 0): self.__OutputStream.write(", ")
        self.__ProfileCount += 1
        
        JSONDump(
            {
                "name" : event.ToString(),
                "cat"  : "Event",
                "ph"   : "i",
                "pid"  : current_process().pid,
                "tid"  : current_thread().native_id,
                "ts"   : TimeConverter.Convert(
                    perf_counter_ns(),
                    TimeConverter.Unit.NenoSecond,
                    TimeConverter.Unit.MicroSecond
                )
            },
            self.__OutputStream
        )

class InstrumentationTimer:
    __Result: ProfileResult
    __Instrumentor: Instrumentor

    def __init__(self, name: str, instrumentor: Instrumentor) -> None:
        # PID & TID are not included here as create overhead and can affect reading
        # They are added in last
        self.__Result = ProfileResult(
            Name=name,
            Start=TimeConverter.Convert(
                perf_counter_ns(),
                TimeConverter.Unit.NenoSecond,
                TimeConverter.Unit.MicroSecond
            )
        )
        self.__Instrumentor = instrumentor

    def Stop(self) -> None:
        if (self.__Result.Complete): return

        self.__Result.End = TimeConverter.Convert(
            perf_counter_ns(),
            TimeConverter.Unit.NenoSecond,
            TimeConverter.Unit.MicroSecond
        )

        self.__Result.PID = current_process().pid         # type: ignore
        self.__Result.TID = current_thread().native_id    # type: ignore

        self.__Result.Complete = True
        
        self.__Instrumentor.WriteProfile(self.__Result)

    def __del__(self) -> None: self.Stop()
