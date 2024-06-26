from ...Events import EventType, MouseButtonPressedEvent, MouseButtonReleasedEvent, MouseMovedEvent
from ...Core.Input import Input
from ...Core.ButtonCodes import *

from .PerspectiveCamera import PerspectiveCamera
from .CameraController import *

from numpy import radians
from typing import Tuple

import pyrr

class PerspectiveCameraController(CameraController):
    __CameraMoveSpeed: float
    __CameraRotationSpeed: float

    __LastMousePosition: Tuple[float, float]
    __MouseClicked: bool

    def __init__(self, camera: PerspectiveCamera) -> None:
        super().__init__(camera)

        self.__CameraMoveSpeed = camera.Speed
        self.__CameraRotationSpeed = 0.075
        self.__LastMousePosition = (0, 0)
        self.__MouseClicked = False

        self._EventDispatcher.AddHandler(EventType.MouseButtonPressed, self.__OnMouseClicked) # type: ignore
        self._EventDispatcher.AddHandler(EventType.MouseButtonReleased, self.__OnMouseReleased) # type: ignore
        self._EventDispatcher.AddHandler(EventType.MouseMoved, self.__OnMouseDragged) # type: ignore

    def __OnMouseClicked(self, e: MouseButtonPressedEvent) -> bool:
        self.__MouseClicked = (e.ButtonCode == MouseCodes.BUTTON_RIGHT)
        if self.__MouseClicked:
            self.__LastMousePosition = Input.GetMousePosition()
            return True

        return False

    def __OnMouseDragged(self, e: MouseMovedEvent) -> bool:
        if not self.__MouseClicked: return False

        delta = ( Input.GetMouseX() - self.__LastMousePosition[0] , Input.GetMouseY() - self.__LastMousePosition[1] )
        self.__LastMousePosition = Input.GetMousePosition()

        self._Camera.Rotation += pyrr.Vector3([ delta[1], delta[0], 0.0 ]) * self.__CameraRotationSpeed
        return True
    
    def __OnMouseReleased(self, e: MouseButtonReleasedEvent) -> bool:
        self.__MouseClicked = e.ButtonCode != MouseCodes.BUTTON_RIGHT
        return False

    def OnUpdate(self, dt: float) -> None:
        # Local Axis
        rotation = pyrr.quaternion.create_from_eulers(radians([ *self._Camera.Rotation ]))
        rotation = pyrr.matrix44.create_from_quaternion(rotation)

        forward, _ = pyrr.vector3.create_from_vector4(rotation[2])
        forward   *= self.__CameraMoveSpeed * dt
        
        right, _ = pyrr.vector3.create_from_vector4(rotation[0])
        right   *= self.__CameraMoveSpeed * dt
        
        up, _ = pyrr.vector3.create_from_vector4(rotation[1])
        up   *= self.__CameraMoveSpeed * dt

        if Input.IsKeyPressed(KeyCodes.W): self._Camera.Translate(-forward) # type: ignore
        elif Input.IsKeyPressed(KeyCodes.S): self._Camera.Translate(forward) # type: ignore

        elif Input.IsKeyPressed(KeyCodes.D): self._Camera.Translate(right) # type: ignore
        elif Input.IsKeyPressed(KeyCodes.D): self._Camera.Translate(-right) # type: ignore

        elif Input.IsKeyPressed(KeyCodes.LEFT_SHIFT): self._Camera.Translate(up) # type: ignore
        elif Input.IsKeyPressed(KeyCodes.LEFT_CONTROL): self._Camera.Translate(-up) # type: ignore
