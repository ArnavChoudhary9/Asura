from typing import List, TypeVar, Type
from abc import ABC, abstractmethod

class Panel(ABC):
    @abstractmethod
    def OnGUIRender(self) -> None: ...

_T = TypeVar("_T")

class PanelManager:
    __Panels: List[Panel]

    def __init__(self) -> None: self.__Panels = []
    def Add(self, panel: Panel): self.__Panels.append(panel)

    def GetPanelOfType(self, _type: Type[_T]) -> _T | None:
        for panel in self.__Panels:
            if isinstance(panel, _type): return panel
        return None

    def OnGUIRender(self) -> None:
        for panel in self.__Panels: panel.OnGUIRender()
