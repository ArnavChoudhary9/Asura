from ..Graphics import *
from ..Utility.Math import Math
from ..Scene import *
from .RenderCommandList import RenderCommandList

class Renderer:
    __Width: int
    __Height: int

    __RenderCommandList: RenderCommandList

    __Framebuffer: SupportsFramebuffer

    def __init__(self, width: int, height: int) -> None:
        self.__Width = width
        self.__Height = height
        self.__RenderCommandList = RenderCommandList()

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

    def Resize(self, width: float, height: float) -> None:
        self.__RenderCommandList.AddCommand(RenderCommands.Resize, width, height)

    def Render(self, scene: Scene) -> None:
        self.__Framebuffer.Bind()
        self.__RenderCommandList.AddCommand(RenderCommands.Clear, 0.3, 0.65, 0.75)
        self.__RenderCommandList.Execute()
        self.__Framebuffer.ClearAttachment(1, Math.PythonInt32ToBytes(69))
        self.__Framebuffer.Unbind()
