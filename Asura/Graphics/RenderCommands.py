from ..Utility import AZ_GRAPHICSLIBRARY, GraphicsLibraryENUM, Protocol, Tuple, List
from ..Logging import CoreLogger
from .RenderCommandList import RenderCommandList

class SupportsRenderCommands(Protocol):
    @staticmethod
    def Clear(*args) -> None: ...
    @staticmethod
    def Resize(x: int, y: int) -> None: ...

class RenderCommands:
    __NativeAPI: SupportsRenderCommands
    __RenderCommandLists: List[RenderCommandList]

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

        else: assert False, CoreLogger.Critical("Unknown Graphics Library: {}", AZ_GRAPHICSLIBRARY)

        RenderCommands.__RenderCommandLists = [ RenderCommandList() ]

    @staticmethod
    def Clear(*args) -> None: RenderCommands.__NativeAPI.Clear(*args)
    @staticmethod
    def Resize(x: int, y: int) -> None: RenderCommands.__NativeAPI.Resize(x, y)

    @staticmethod
    # Return a free RenderCommandList else return None
    def GetFreeCommandList() -> RenderCommandList | None:
        for _list in RenderCommands.__RenderCommandLists:
            if not _list.IsFree: continue

            _list.Lock()
            return _list

        return None
