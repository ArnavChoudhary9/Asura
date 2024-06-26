import pyrr
from abc import ABC, abstractmethod
from math import radians

class Camera(ABC):
    _ProjectionMatrix: pyrr.Matrix44
    _ViewMatrix: pyrr.Matrix44

    _ViewProjectionMatrix: pyrr.Matrix44

    _Position: pyrr.Vector3
    _Rotation: pyrr.Vector3

    _AspectRatio: float

    def __init__(self, view: pyrr.Matrix44, projection: pyrr.Matrix44, aspectRatio: float) -> None:
        self._ViewMatrix = view
        self._ProjectionMatrix = projection
        self._ViewProjectionMatrix = view @ projection # type: ignore

        self._AspectRatio = aspectRatio

        self._Position = pyrr.Vector3([0.0, 0.0, 0.0])
        self._Rotation = pyrr.Vector3([0.0, 0.0, 0.0])

        self._RecalculateViewMatrix()

    def _RecalculateViewMatrix(self) -> None:
        transform: pyrr.Matrix44 = pyrr.matrix44.create_from_translation(self._Position) # type: ignore
        rotation: pyrr.Matrix44 = pyrr.matrix44.create_from_eulers(self._Rotation) # type: ignore

        model = rotation @ transform
        self._ViewMatrix = pyrr.matrix44.inverse(model)
        self._ViewProjectionMatrix = self._ViewMatrix @ self._ProjectionMatrix # type: ignore

    @property
    def Position(self) -> pyrr.Vector3: return self._Position

    @Position.setter
    def Position(self, position: pyrr.Vector3) -> None:
        if not isinstance(position, pyrr.Vector3): raise ValueError("Position must be a pyrr.Vector3")
        self._Position = position
        self._RecalculateViewMatrix()

    def Translate(self, delta: pyrr.Vector3) -> None: self.Position += delta

    @property
    def Rotation(self) -> pyrr.Vector3: return self._Rotation

    @Rotation.setter
    def Rotation(self, rotation: pyrr.Vector3) -> None:
        if not isinstance(rotation, pyrr.Vector3): raise ValueError("Rotation must be a pyrr.Vector3")
        self._Rotation = rotation
        self._RecalculateViewMatrix()

    @property
    def ProjectionMatrix(self) -> pyrr.Matrix44: return self._ProjectionMatrix
    @property
    def ViewMatrix(self) -> pyrr.Matrix44: return self._ViewMatrix
    @property
    def ViewProjectionMatrix(self) -> pyrr.Matrix44: return self._ViewProjectionMatrix

    @property
    def AspectRatio(self) -> float: return self._AspectRatio

    @AspectRatio.setter
    def AspectRatio(self, aspectRatio: float) -> None:
        if not isinstance(aspectRatio, float): raise ValueError("Aspect ratio must be a float")
        self._AspectRatio = aspectRatio
        self._RecalculateViewMatrix()

    @property
    @abstractmethod
    def Speed(self) -> float: ...
