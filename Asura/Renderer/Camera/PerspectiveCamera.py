from .Camera import Camera

import pyrr

class PerspectiveCamera(Camera):
    _FOV: float
    _Near: float
    _Far: float

    def __init__(self, fov: float, aspectRatio: float, near: float=0.01, far: float=1000) -> None:
        self._FOV = fov
        self._Near = near
        self._Far = far

        viewMatrix: pyrr.Matrix44 = pyrr.matrix44.create_identity() # type: ignore
        projectionMatrix: pyrr.Matrix44 = pyrr.matrix44.create_perspective_projection_matrix(
            fov, aspectRatio, near, far
        ) # type: ignore

        super().__init__(viewMatrix, projectionMatrix, aspectRatio)

    @property
    def FOV(self) -> float: return self._FOV
    @property
    def AspectRatio(self) -> float: return self._AspectRatio

    @AspectRatio.setter
    def AspectRatio(self, value: float) -> None:
        if not isinstance(value, float): raise ValueError("AspectRatio must be a float")

        self._AspectRatio = value
        self.RecalculateProjectionMatrix()

    @FOV.setter
    def FOV(self, value: float) -> None:
        if not isinstance(value, float): raise ValueError("FOV must be a float")
        self._FOV = value+0.001 # ???
        self.RecalculateProjectionMatrix()

    def RecalculateProjectionMatrix (self) -> None:
        self._ProjectionMatrix = pyrr.matrix44.create_perspective_projection_matrix(
            self._FOV, self._AspectRatio, self._Near, self._Far
        ) # type: ignore

        self._RecalculateViewMatrix()

    @property
    def Speed(self) -> float: return self._FOV / 15
