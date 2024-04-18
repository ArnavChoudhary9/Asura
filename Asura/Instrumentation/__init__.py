from ..Utility.Constants import AZ_INSTRUMENTATION
from .Instrumentation import Instrumentor, InstrumentationTimer     # type: ignore

from functools import partial

ASURA_INSTRUMENTATION_VERSION: tuple = (2,1,0)
ASURA_INSTRUMENTATION_VERSION_STR: str = ".".join(
    [str(s) for s in ASURA_INSTRUMENTATION_VERSION]
)

if not AZ_INSTRUMENTATION:
    class Instrumentor:
        def BeginSession(self, name: str) -> None: pass
        def EndSession(self) -> None: pass
        def WriteEvent(self, event) -> None: pass

    class InstrumentationTimer:
        def __init__(self, name: str, instrumentor: Instrumentor) -> None: pass
        def Stop(self): pass

InstrumentorObj = Instrumentor()
Timer = partial(InstrumentationTimer, instrumentor=InstrumentorObj)

def PrintInstrumentationSystem() -> None:
    print("Instrumentation System Online\nVersion: {}".format(ASURA_INSTRUMENTATION_VERSION_STR))
    print("-"*50)
