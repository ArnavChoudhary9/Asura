from .Camera import Camera

import pyrr

class OrthographicCamera(Camera):
    _Scale: float
    _Near: float
    _Far: float
    _Rotation: float

    def __init__(self, scale: float, aspectRatio: float) -> None:
        self._Scale = scale
        self._Near = 0.1
        self._Far = 1000
        _Rotation = 0.0

        viewMatrix: pyrr.Matrix44 = pyrr.matrix44.create_identity() # type: ignore
        projectionMatrix: pyrr.Matrix44 = pyrr.matrix44.create_perspective_projection_matrix(
            scale, aspectRatio, self._Near, self._Far
        ) # type: ignore

        super().__init__(viewMatrix, projectionMatrix, aspectRatio)

    @property
    def Scale(self) -> float: return self._Scale
    @property
    def AspectRatio(self) -> float: return self._AspectRatio
    @property
    def Rotation(self) -> float: return self._Rotation

    @Rotation.setter
    def Rotation(self, rotation: float) -> None:
        if not isinstance(rotation, float): raise ValueError("Rotation must be a float")
        self._Rotation = rotation
        self._RecalculateViewMatrix()

    @AspectRatio.setter
    def AspectRatio(self, value: float) -> None:
        if not isinstance(value, float): raise ValueError("AspectRatio must be a float")

        self._AspectRatio = value
        self.RecalculateProjectionMatrix()

    @Scale.setter
    def Scale(self, value: float) -> None:
        if not isinstance(value, float): raise ValueError("Scale must be a float")

        self._Scale = value
        self.RecalculateProjectionMatrix()

    def RecalculateProjectionMatrix (self) -> None:
        self._ProjectionMatrix = pyrr.matrix44.create_orthogonal_projection_matrix(
            -self.AspectRatio * self._Scale,
            self.AspectRatio * self._Scale,
            -self._Scale, self._Scale, self._Near, self._Far
        ) # type: ignore
        self._RecalculateViewMatrix()

    @property
    def Speed(self) -> float: return self._Scale * 1.25
