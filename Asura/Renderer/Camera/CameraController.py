from ...Core.ButtonCodes import *
from ...Events import Event, WindowResizeEvent, EventDispatcher, EventType

from .Camera import Camera

from abc import ABC, abstractmethod

class CameraController(ABC):
    _Camera: Camera
    _EventDispatcher: EventDispatcher

    def __init__(self, camera: Camera) -> None:
        self._Camera = camera
        self._EventDispatcher = EventDispatcher()

        self._EventDispatcher.AddHandler(EventType.WindowResize, self._OnWindowResize) # type: ignore

    @property
    def Camera(self) -> Camera: return self._Camera

    @abstractmethod
    def OnUpdate(self, dt: float) -> None: ...

    def OnEvent(self, e: Event) -> None: self._EventDispatcher.Dispatch(e)
    def _OnWindowResize(self, e: WindowResizeEvent) -> None: self._Camera.AspectRatio = e.Width / e.Height
