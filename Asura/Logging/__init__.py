from .Logger import * # type: ignore
from ..Utility.Constants import AZ_LOGGING

ASURA_LOGGER_VERSION: tuple = (2,2,0)
ASURA_LOGGER_VERSION_STR: str = ".".join(
    [str(s) for s in ASURA_LOGGER_VERSION]
)

if not AZ_LOGGING:
    class Logger:
        def __init__(self, name: str, logPattern: str="%^[%T] %n: %v%$") -> None: pass

        @property
        def Name(self) -> str: return ""
        
        def Trace    (self, msg: str, *args) -> None: pass
        def Info     (self, msg: str, *args) -> None: pass
        def Debug    (self, msg: str, *args) -> None: pass
        def Warn     (self, msg: str, *args) -> None: pass
        def Error    (self, msg: str, *args) -> None: pass
        def Critical (self, msg: str, *args) -> None: pass

    class LoggerSubscription:
        def __init__(self) -> None: pass

        def Subscribe   (self, logger: Logger) -> None: pass
        def Unsubscribe (self, logger: Logger) -> None: pass

        def Trace    (self, msg: str, *args) -> None:  pass
        def Info     (self, msg: str, *args) -> None: pass
        def Debug    (self, msg: str, *args) -> None: pass
        def Warn     (self, msg: str, *args) -> None: pass
        def Error    (self, msg: str, *args) -> None: pass
        def Critical (self, msg: str, *args) -> None: pass


else: Logger.INIT()

ClientLoggers: LoggerSubscription = LoggerSubscription()

CoreLogger: Logger = Logger("ASURA")
ClientLoggers.Subscribe(Logger("CLIENT")) # type: ignore

def PrintLogging() -> None:
    print("Logging System Online\nVersion: {}".format(ASURA_LOGGER_VERSION_STR))
    print("-"*50)
