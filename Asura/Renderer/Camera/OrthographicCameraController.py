from ..Camera.OrthographicCamera import *
from ...Events import EventDispatcher, EventType, MouseScrolledEvent

from ...Core.Input import *
from ...Core.ButtonCodes import *

from .CameraController import CameraController

class OrthographicCameraController(CameraController):
    __CameraMoveSpeed: float
    __CameraRotationSpeed: float

    def __init__(self, camera: OrthographicCamera) -> None:
        super().__init__(camera)

        self.__CameraMoveSpeed = camera.Speed
        self.__CameraRotationSpeed = 135

        def MouseScrollHandler(e: MouseScrolledEvent) -> None: self._Camera.Speed = self._Camera.Scale - (e.OffsetY * 0.05) + 0.001 # type: ignore
        self._EventDispatcher.AddHandler(EventType.MouseScrolled, MouseScrollHandler) # type: ignore

        self.__CameraMoveSpeed = self._Camera.Speed

    def OnUpdate(self, dt: float) -> None:
        posDelta = pyrr.Vector3([ 0.0, 0.0, 0.0 ])
        if Input.IsKeyPressed(KeyCodes.W): posDelta = pyrr.Vector3([ 0.0, 1.0, 0.0 ])
        elif Input.IsKeyPressed(KeyCodes.S): posDelta = -pyrr.Vector3([ 0.0, 1.0, 0.0 ])
        elif Input.IsKeyPressed(KeyCodes.A): posDelta = pyrr.Vector3([ 1.0, 0.0, 0.0 ])
        elif Input.IsKeyPressed(KeyCodes.D): posDelta = -pyrr.Vector3([ 1.0, 0.0, 0.0 ])
        self._Camera.Position += posDelta * self.__CameraMoveSpeed * dt

        rotDelta = 0
        if Input.IsKeyPressed(KeyCodes.Q): rotDelta = -1
        elif Input.IsKeyPressed(KeyCodes.E): rotDelta = 1
        self._Camera.Rotation += rotDelta * self.__CameraRotationSpeed * dt
