import spdlog
from ..Utility import *

# This will be the logger if AZ_LOGGING is disabled
# It does not do anything, it's just a placeholder
class DummyLogger:
    def trace    (self, *args) -> None: pass
    def info     (self, *args) -> None: pass
    def debug    (self, *args) -> None: pass
    def warn     (self, *args) -> None: pass
    def error    (self, *args) -> None: pass
    def critical (self, *args) -> None: pass

class Logger:
    @classmethod
    def INIT(cls):
        cls.__LogSinks = [
            spdlog.stdout_color_sink_mt(),
            spdlog.basic_file_sink_mt("Asura.log", True)
        ]

    __slots__ = "__Name", "__Logger"

    def __init__(self, name: str, logPattern: str="%^[%T] %n: %v%$") -> None:
        self.__Name: str = name

        if AZ_LOGGING:
            self.__Logger = spdlog.SinkLogger(name, Logger.__LogSinks)
            self.__Logger.set_pattern(logPattern)
            self.__Logger.set_level(spdlog.LogLevel.TRACE)
            self.__Logger.flush_on(spdlog.LogLevel.TRACE)
        
        # Select the "Do nothing" logger if AZ_LOGGING is disabled
        else: self.__Logger = DummyLogger()

        self.Info("Logger *{}* Initialized!", name)

    @property
    def Name(self) -> str: return self.__Name
    
    def Trace    (self, msg: str, *args) -> None: self.__Logger.trace    (msg.format(*args))
    def Info     (self, msg: str, *args) -> None: self.__Logger.info     (msg.format(*args))
    def Debug    (self, msg: str, *args) -> None: self.__Logger.debug    (msg.format(*args))
    def Warn     (self, msg: str, *args) -> None: self.__Logger.warn     (msg.format(*args))
    def Error    (self, msg: str, *args) -> None: self.__Logger.error    (msg.format(*args))
    def Critical (self, msg: str, *args) -> None: self.__Logger.critical (msg.format(*args))

class LoggerSubscription:  
    '''
    This is basically a wrapper around a list that contains many Loggers.
    The message sent to it will be distributed to all the loggers that have subscribed to it.

    Usage::

        loggers = LoggerSubscription()
        loggers.Subscribe(Logger("A"))
        loggers.Subscribe(Logger("B"))
        loggers.Trace("TEST") # Calling Trace only once

    Will produce::

        [hh:mm:ss] A: TEST
        [hh:mm:ss] B: TEST
    '''

    __slots__ = "__Subscriptions"
    __Subscriptions: List[Logger]

    def __init__(self) -> None: self.__Subscriptions: List[Logger] = []

    def Subscribe   (self, logger: Logger) -> None: self.__Subscriptions.append(logger)
    def Unsubscribe (self, logger: Logger) -> None: self.__Subscriptions.remove(logger)

    def Trace(self, msg: str, *args) -> None: 
        for logger in self.__Subscriptions: logger.Trace(msg, *args)

    def Info(self, msg: str, *args) -> None:
        for logger in self.__Subscriptions: logger.Info(msg, *args)

    def Debug(self, msg: str, *args) -> None:
        for logger in self.__Subscriptions: logger.Debug(msg, *args)

    def Warn(self, msg: str, *args) -> None:
        for logger in self.__Subscriptions: logger.Warn(msg, *args)

    def Error(self, msg: str, *args) -> None:
        for logger in self.__Subscriptions: logger.Error(msg, *args)
        
    def Critical(self, msg: str, *args) -> None:
        for logger in self.__Subscriptions: logger.Critical(msg, *args)