from ..Graphics import *
from ..Utility.Math import Math
from ..Scene import *

class Renderer:
    __Width: int
    __Height: int

    __Framebuffer: SupportsFramebuffer

    __RenderCommandList: RenderCommandList
    __Scene: Scene

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

    def Resize(self, width: float, height: float) -> None:
        self.__RenderCommandList.AddCommand(RenderCommands.Resize, width, height)

    def BeginScene(self, scene: Scene) -> None:
        commandList = None
        while not commandList:
            commandList = RenderCommands.GetFreeCommandList()

        self.__RenderCommandList = commandList
        self.__Scene = scene
        self.__Framebuffer.Bind()

    def Render(self) -> None:
        self.__RenderCommandList.AddCommand(RenderCommands.Clear, 0.3, 0.65, 0.75)
        self.__Framebuffer.ClearAttachment(1, Math.PythonInt32ToBytes(69))
        self.__RenderCommandList.Execute()

    def EndScene(self) -> None:
        self.__Framebuffer.Unbind()
