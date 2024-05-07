from ..Utility import DataClass, Tuple
from ..Utility import TextureConstants, GraphicsLibraryENUM, AZ_GRAPHICSLIBRARY, Type, UUID, UUID4Generator
from ..Logging import CoreLogger

from abc import ABC, abstractmethod

@DataClass
class TextureSpecification:
    TextureFormat: int = TextureConstants.Format.RGBA
    TextureSize: int = TextureConstants.Size.RGBA8
    DataType: int = TextureConstants.DataType.UNSIGNED_BYTE

    WrapS: int = TextureConstants.WrapMode.REPEAT
    WrapT: int = TextureConstants.WrapMode.REPEAT
    WrapR: int = TextureConstants.WrapMode.REPEAT

    MagFilter: int = TextureConstants.Filter.LINEAR
    MinFilter: int = TextureConstants.Filter.LINEAR

    Multisample: bool = False

class Texture(ABC):
    @staticmethod
    def Init() -> None:
        Texture2D.Init()

    @property
    @abstractmethod
    def RendererID(self) -> int: ...

    @property
    @abstractmethod
    def Specifications(self) -> TextureSpecification: ...

    @property
    @abstractmethod
    def TextureUUID(self) -> int: ...

    @property
    @abstractmethod
    def Width(self) -> int: ...

    @property
    @abstractmethod
    def Height(self) -> int: ...

    @property
    @abstractmethod
    def Dimension(self) -> Tuple[int, int]: ...

    @abstractmethod
    # TODO: Set data and size types.
    # WARNING: C000 not followed. 
    def SetData(self, data: bytes, size) -> None: ...

    @abstractmethod
    def Bind(self, slot: int=0) -> None: ...

    @abstractmethod
    def Unbind(self) -> None: ...

class Texture2D(Texture):
    __NativeAPI: Type[Texture]

    @staticmethod
    def Init() -> None:
        '''
        Detects the desired Graphics Library, and saves Texture2D.
        '''

        if AZ_GRAPHICSLIBRARY == GraphicsLibraryENUM.Headless:
            assert False, CoreLogger.Critical("GraphicsLibraryENUM.Headless not supported Yet!!")

        elif AZ_GRAPHICSLIBRARY == GraphicsLibraryENUM.OpenGL:
            from .OpenGL.OpenGLTexture2D import OpenGLTexture2D
            Texture2D.__NativeAPI = OpenGLTexture2D

        else: assert False, CoreLogger.Critical("Unknown Graphics Library: {}", AZ_GRAPHICSLIBRARY)
    
    @staticmethod
    def Create(width: int, height: int, spec: TextureSpecification) -> Texture:
        return Texture2D.__NativeAPI(width, height, spec)
