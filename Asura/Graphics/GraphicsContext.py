from ..Utility import AZ_GRAPHICSLIBRARY, GraphicsLibraryENUM, Protocol, runtime_checkable
from ..Logging import CoreLogger

from abc import ABC, abstractmethod

@runtime_checkable
class SuppurtsGraphicsContext(Protocol):
    @abstractmethod
    def Init(self) -> None: ...
    @abstractmethod
    def SwapBuffers(self) -> None: ...

class GraphicsContext(ABC):
    _WindowHandle: int

    def __init__(self, windowHandle: int) -> None:
        self._WindowHandle = windowHandle

    @abstractmethod
    def Init(self) -> None: ...
    @abstractmethod
    def SwapBuffers(self) -> None: ...

    @staticmethod
    def Create(windowHandle: int) -> SuppurtsGraphicsContext:
        '''
        Detects the desired Graphics Library, and returns the appropriate Graphics Context.
        '''

        if AZ_GRAPHICSLIBRARY == GraphicsLibraryENUM.Headless:
            assert False, CoreLogger.Critical("GraphicsLibraryENUM.Headless not supported Yet!!")

        elif AZ_GRAPHICSLIBRARY == GraphicsLibraryENUM.OpenGL:
            from .OpenGL.OpenGLGraphicsContext import OpenGLGraphicsContext
            return OpenGLGraphicsContext(windowHandle)

        else: assert False, CoreLogger.Critical("Unknown Graphics Library: {}", AZ_GRAPHICSLIBRARY)
