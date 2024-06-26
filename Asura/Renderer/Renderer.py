from ..Graphics import *
from ..Utility.Math import Math
from ..Scene import *

from .Camera import *

from dataclasses import dataclass

@dataclass(frozen=True)
class RenderData:
    Scene: Scene
    Camera: Camera

class Renderer:
    __Width: int
    __Height: int

    __Framebuffer: SupportsFramebuffer

    __RenderCommandList: RenderCommandList
    __RenderData: RenderData

    def __init__(self, width: int, height: int) -> None:
        self.__Width = width
        self.__Height = height

        framebufferSpecs = FramebufferSpecification(self.__Width, self.__Height)

        framebufferSpecs.AddAttachment(TextureSpecification())

        redIntBufferSpecs = TextureSpecification()
        redIntBufferSpecs.TextureFormat = TextureConstants.Format.RED_INTEGER
        redIntBufferSpecs.TextureSize = TextureConstants.Size.R32I
        framebufferSpecs.AddAttachment(redIntBufferSpecs)

        depthBufferSpecs = TextureSpecification()
        depthBufferSpecs.TextureFormat = TextureConstants.Format.DEPTH_STENCIL
        depthBufferSpecs.TextureSize = TextureConstants.Size.DEPTH24STENCIL8
        depthBufferSpecs.DataType = TextureConstants.DataType.UNSIGNED_INT_24_8
        framebufferSpecs.AddAttachment(depthBufferSpecs)

        self.__Framebuffer = Framebuffer.Create(framebufferSpecs)

        RenderCommands.INIT()

    @property
    def Framebuffer(self) -> SupportsFramebuffer: return self.__Framebuffer
    @property
    def Dimensions(self) -> Tuple[int, int]: return self.__Width, self.__Height

    def Resize(self, width: int, height: int) -> None:
        self.__RenderCommandList.AddCommand(RenderCommands.Resize, width, height)
        self.__Framebuffer.Resize(width, height)
        self.__RenderData.Camera.AspectRatio = width / height

    def BeginScene(self, scene: Scene, camera: Camera) -> None:
        commandList = None
        while not commandList:
            commandList = RenderCommands.GetFreeCommandList()

        self.__RenderCommandList = commandList
        self.__RenderData = RenderData(scene, camera)
        self.__Framebuffer.Bind()

    def Render(self) -> None:
        self.__RenderCommandList.AddCommand(RenderCommands.Clear, 0.3, 0.65, 0.75)
        self.__Framebuffer.ClearAttachment(1, Math.PythonInt32ToBytes(0))

    def EndScene(self) -> None:
        self.__RenderCommandList.Execute()
        self.__Framebuffer.Unbind()

        del self.__RenderData
