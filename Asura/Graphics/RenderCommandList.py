from ..Utility import PartialFunction, List, Callable
from ..Logging import CoreLogger

class RenderCommandList:
    __List: List[Callable[[], None]]

    __Locked: bool
    __Filled: bool

    def __init__(self) -> None:
        self.__List = []
        self.__Locked = False
        self.__Filled = False

    # (not A) and (not B) => not (A or B)
    @property
    def IsFree(self) -> bool: return not (self.__Locked or self.__Filled)

    def AddCommand(self, func: Callable, *args, **kwargs) -> None:
        assert self.__Locked, CoreLogger.Error("RenderCommandList must be locked before adding commands")
        self.__Filled = True
        self.__List.append(PartialFunction(func, *args, **kwargs))

    def Lock(self) -> None: self.__Locked = True
    def Unlock(self) -> None: self.__Locked = False

    def Execute(self) -> None:
        for command in self.__List: command()
        self.__List.clear()
        self.__Filled = False
        self.Unlock()
