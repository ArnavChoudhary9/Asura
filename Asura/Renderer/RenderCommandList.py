from ..Utility import PartialFunction, List, Callable

class RenderCommandList:
    __List: List[Callable[[], None]]

    def __init__(self) -> None:
        self.__List = []

    def AddCommand(self, func: Callable, *args, **kwargs) -> None:
        self.__List.append(PartialFunction(func, *args, **kwargs))

    def Execute(self) -> None:
        for command in self.__List: command()
        self.__List.clear()
