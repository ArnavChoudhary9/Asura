from .Logger import *

ASURA_LOGGER_VERSION: tuple = (2,1,0)
ASURA_LOGGER_VERSION_STR: str = ".".join(
    [str(s) for s in ASURA_LOGGER_VERSION]
)

Logger.INIT()

ClientLoggers: LoggerSubscription = LoggerSubscription()

CoreLogger: Logger = Logger("ASURA")
ClientLoggers.Subscribe(Logger("CLIENT"))

def PrintLogging() -> None:
    print("Logging Module Online\nVersion: {}".format(ASURA_LOGGER_VERSION_STR))
    print("-"*50)
