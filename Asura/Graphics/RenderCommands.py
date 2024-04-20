from ..Utility import AZ_GRAPHICSLIBRARY, GraphicsLibraryENUM, Protocol, Tuple
from ..Logging import CoreLogger

class SupportsRenderCommands(Protocol):
    @classmethod
    def Clear(cls, *args) -> None: ...

class RenderCommands:
    __NativeAPI: SupportsRenderCommands

    @staticmethod
    def INIT() -> None:
        '''
        Detects the desired Graphics Library, and initializes the render commands.
        '''

        if AZ_GRAPHICSLIBRARY == GraphicsLibraryENUM.Headless:
            assert False, CoreLogger.Critical("GraphicsLibraryENUM.Headless not supported Yet!!")

        elif AZ_GRAPHICSLIBRARY == GraphicsLibraryENUM.OpenGL:
            from .OpenGL.OpenGLRenderCommands import OpenGLRenderCommands
            RenderCommands.__NativeAPI = OpenGLRenderCommands
            return

        else: assert False, CoreLogger.Critical("Unknown Graphics Library: {}", AZ_GRAPHICSLIBRARY)

    @staticmethod
    def Clear(*args) -> None: RenderCommands.__NativeAPI.Clear(*args)
