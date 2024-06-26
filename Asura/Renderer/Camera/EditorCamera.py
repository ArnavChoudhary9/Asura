from ...Core import KeyCodes, MouseCodes, Input

from .PerspectiveCamera import PerspectiveCamera

from typing import Tuple
import pyrr

def CLAMP(minValue: float, maxValue: float, value: float) -> float: return sorted((minValue, value, maxValue))[1]

class EditorCamera(PerspectiveCamera):
    __FocalPoint: pyrr.Vector3

    __InitialMousePosition: Tuple[float, float]

    __Distance: float
    __Pitch: float
    __Yaw: float

    __ViewportWidth: float = 1280
    __ViewportHeight: float = 720
    
    def __init__(self, fov: float, aspectRatio: float, near: float=0.1, far: float=1000) -> None:
        self._Reset()
        super().__init__(fov, aspectRatio, near, far)
        self._Recaclulate()

    @property
    def Distance(self) -> float: return self.__Distance
    @Distance.setter
    def Distance(self, value: float):
        if not isinstance(value, float): raise ValueError("Distance must be a float")
        self.__Distance = value

    def SetViewportSize(self, width: float, height: float) -> None:
        self.__ViewportWidth = width
        self.__ViewportHeight = height
        self.AspectRatio = width / height

    @property
    def Forward(self) -> pyrr.Vector3:
        orientation = pyrr.matrix44.create_from_quaternion(self.Orientation)
        return pyrr.vector3.create_from_vector4(orientation[2])[0] # type: ignore
    
    @property
    def Right(self) -> pyrr.Vector3:
        orientation = pyrr.matrix44.create_from_quaternion(self.Orientation)
        return pyrr.vector3.create_from_vector4(orientation[0])[0] # type: ignore
    
    @property
    def Up(self) -> pyrr.Vector3:
        orientation = pyrr.matrix44.create_from_quaternion(self.Orientation)
        return pyrr.vector3.create_from_vector4(orientation[1])[0] # type: ignore
    
    @property
    def Orientation(self) -> pyrr.Quaternion:
        return pyrr.quaternion.create_from_eulers([ -self.__Pitch, -self.__Yaw, 0.0 ]) # type: ignore
    
    @property
    def Position(self) -> pyrr.Vector3: return self.__FocalPoint - self.Forward * self.__Distance

    @property
    def Pitch(self) -> float: return self.__Pitch
    @property
    def Yaw(self) -> float: return self.__Yaw

    @property
    def __PanSpeed(self) -> Tuple[float, float]:
        x = min(self.__ViewportWidth / 1000, 0.2)
        xFactor = 0.0145 * (x*x) - (self.AspectRatio/10) * x + 0.2

        y = min(self.__ViewportHeight / 1000, 0.2)
        yFactor = 0.0145 * (y*y) - (self.AspectRatio/10) * y + 0.2

        return xFactor, yFactor

    @property
    def __RotationSpeed(self) -> float: return 0.1

    @property
    def __ZoomSpeed(self) -> float:
        distance = max(abs(self.__Distance * 0.1), 0.001)
        speed = 1/distance * 0.9
        return CLAMP(7.5, speed, 100)

    def _Reset(self) -> None:
        self.__InitialMousePosition = (0, 0)

        self.__FocalPoint = pyrr.Vector3([ 0.0, 0.0, 0.0 ])

        self.__Distance = -5.0
        self.__Pitch = 0.0
        self.__Yaw = 0.0

    def _Recaclulate(self) -> None:
        self._ViewMatrix = pyrr.matrix44.inverse(
            pyrr.matrix44.create_from_quaternion(self.Orientation) @ pyrr.matrix44.create_from_translation(self.Position)
        )
        self._ViewProjectionMatrix = self._ViewMatrix @ self._ProjectionMatrix # type: ignore

    def __MousePan(self, delta: Tuple[float, float]) -> None:
        xSpeed, ySpeed = self.__PanSpeed
        self.__FocalPoint -= self.Right * delta[0] * xSpeed * self.__Distance
        self.__FocalPoint += self.Up * delta[1] * ySpeed * self.__Distance

    def __MouseRotate(self, delta: Tuple[float, float]) -> None:
        yawSign = self.Up[1] / abs(self.Up[1])
        self.__Yaw += yawSign * delta[0] * self.__RotationSpeed
        self.__Pitch += delta[1] * self.__RotationSpeed

    def __MouseZoom(self, delta: float) -> None: self.__Distance -= delta * self.__ZoomSpeed

    def OnUpdate(self, dt: float):
        if not Input.IsKeyPressed(KeyCodes.LEFT_ALT): return

        mouse = Input.GetMousePosition()
        delta = (
            (self.__InitialMousePosition[0] - mouse[0]) * dt,
            (self.__InitialMousePosition[1] - mouse[1]) * dt
        )

        self.__InitialMousePosition = mouse

        if   Input.IsMouseButtonPressed(MouseCodes.BUTTON_MIDDLE) : self.__MousePan(delta)
        elif Input.IsMouseButtonPressed(MouseCodes.BUTTON_LEFT)   : self.__MouseRotate(delta)
        elif Input.IsMouseButtonPressed(MouseCodes.BUTTON_RIGHT)  : self.__MouseZoom(delta[1])

        self._Recaclulate()
