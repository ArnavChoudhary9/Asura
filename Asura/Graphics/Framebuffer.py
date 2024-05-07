from ..Utility import List, Type, Protocol, Tuple
from ..Utility.Constants import AZ_GRAPHICSLIBRARY, GraphicsLibraryENUM
from ..Logging import CoreLogger
from .Texture import *

from abc import ABC, abstractmethod

class FramebufferSpecification:
    Width: int
    Height: int

    Attachments: List[TextureSpecification]

    Samples: int = 1
    SwapChainTarget: bool = False

    def __init__(self, width: int, height: int) -> None:
        self.Width = width
        self.Height = height
        self.Attachments = []

    @property
    def Dimensions(self) -> Tuple[int, int]: return (self.Width, self.Height)

    def AddAttachment(self, attachment: TextureSpecification) -> None:
        self.Attachments.append(attachment)

class SupportsFramebuffer(Protocol):
    def __init__(self, specs: FramebufferSpecification) -> None: ...
    def Bind(self) -> None: ...
    def ClearAttachment(self, index: int, value: bytes) -> None: ...
    def GetColorAttachment(self, index: int=0) -> Texture: ...
    def Unbind(self) -> None: ...
    def Resize(self, width: int, height: int) -> None: ...
    def ReadPixel(self, index: int, x: int, y: int) -> bytes: ...

    @property
    def Specifications(self) -> FramebufferSpecification: ...

class Framebuffer(ABC):
    __NativeAPI: Type[SupportsFramebuffer]

    @staticmethod
    def Init() -> None:
        '''
        Detects the desired Graphics Library, and saves Framebuffer.
        '''

        if AZ_GRAPHICSLIBRARY == GraphicsLibraryENUM.Headless:
            assert False, CoreLogger.Critical("GraphicsLibraryENUM.Headless not supported Yet!!")

        elif AZ_GRAPHICSLIBRARY == GraphicsLibraryENUM.OpenGL:
            from .OpenGL.OpenGLFramebuffer import OpenGLFramebuffer
            Framebuffer.__NativeAPI = OpenGLFramebuffer

        else: assert False, CoreLogger.Critical("Unknown Graphics Library: {}", AZ_GRAPHICSLIBRARY)
    
    @abstractmethod
    def Bind(self) -> None: ...
    @abstractmethod
    def ClearAttachment(self, index: int, value: bytes) -> None: ...
    @abstractmethod
    def GetColorAttachment(self, index: int=0) -> Texture: ...
    @abstractmethod
    def Unbind(self) -> None: ...
    @abstractmethod
    def Resize(self, width: int, height: int) -> None: ...
    @abstractmethod
    def ReadPixel(self, index: int, x: int, y: int): ...

    def __enter__ (self)        -> None: self.Bind()
    def __exit__  (self, *args) -> None: self.Unbind()

    @staticmethod
    def Create(specs: FramebufferSpecification) -> SupportsFramebuffer:
        return Framebuffer.__NativeAPI(specs)
