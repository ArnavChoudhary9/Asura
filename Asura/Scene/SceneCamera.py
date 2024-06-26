from ..Renderer.Camera import *

from enum import Enum

class ProjectionTypes(Enum):
    ORTHOGRAPHIC = 1
    PERSPECTIVE  = 2

class SceneCamera:
    __ProjectionType: Enum
    __Camera: Camera

    def __init__(self, projectionType: Enum=ProjectionTypes.ORTHOGRAPHIC) -> None:
        self.SetProjectionType(projectionType)

    @property
    def ProjectionType(self) -> Enum: return self.__ProjectionType
    @property
    def CameraObject(self) -> Camera: return self.__Camera

    def _Recalculate(self) -> None:
        if not self.__Camera:
            if self.__ProjectionType == ProjectionTypes.ORTHOGRAPHIC:
                self.__Camera = OrthographicCamera(1, 1)
            elif self.__ProjectionType == ProjectionTypes.PERSPECTIVE:
                self.__Camera = PerspectiveCamera(60, 1)

        self.__Camera._RecalculateViewMatrix()

    def SetProjectionType(self, projectionType: Enum) -> None:
        self.__ProjectionType = projectionType

        aspectRatio = 0
        if self.__Camera:
            aspectRatio = self.__Camera.AspectRatio
            del self.__Camera

        self._Recalculate()
        if aspectRatio: self.__Camera.AspectRatio = aspectRatio
