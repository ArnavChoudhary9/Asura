from ..Utility import *
from ..Events  import *

from abc import ABC, abstractmethod

class Layer(ABC):
    __slots__ = "_Name", "_Enabled", "_EventDispatcher"
    _Name: str
    _Enabled: bool
    _EventDispatcher: EventDispatcher

    def __init__(self, name: str="Layer") -> None:
        self._Name = name
        self._Enabled = True
        self._EventDispatcher = EventDispatcher()
        self.OnInitialize()

    def __str__(self) -> str:
        return "<Layer @ {}>: {}".format(hex(id(self)), self._Name)
    def ToString(self) -> str: return str(self)

    @property
    def Name(self) -> str: return self._Name
    @property
    def Enabled(self) -> bool: return self._Enabled

    def ToggleEnable(self) -> bool:
        self._Enabled = not self._Enabled
        return self._Enabled
    
    def SetEnable(self, enable: bool) -> None: self._Enabled = enable
    
    # No need to handle this in LayerStack,
    # It is called of layer itself in __init__
    @abstractmethod
    def OnInitialize(self) -> None: ...
    # You should bind all the event handlers in this or OnStart() method

    @abstractmethod
    def OnStart(self) -> None: ...

    @abstractmethod
    def OnUpdate(self, dt: float) -> None: ... # C003

    @abstractmethod
    def OnStop(self) -> None: ...

    @abstractmethod
    def OnDestroy(self) -> None: ...
    
    # Return weather event has been handled by the Layer
    def OnEvent(self, event: Event) -> bool: return self._EventDispatcher.Dispatch(event)

class Overlay(Layer):
    def __init__(self, name: str="Overlay") -> None:
        super().__init__(name)

    def __str__(self) -> str:
        return "<Overlay @ {}>: {}".format(hex(id(self)), self._Name)

    @abstractmethod
    def OnGUIStart(self) -> None: ...

    @abstractmethod
    def OnGUIRender(self) -> None: ...

    @abstractmethod
    def OnGUIEnd(self) -> None: ...
