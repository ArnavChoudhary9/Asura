from ..Graphics import *
from ..Scene import *
from .RenderCommandList import RenderCommandList

class Renderer:
    __Width: float
    __Height: float

    __RenderCommandList: RenderCommandList

    def __init__(self, width: float, height: float) -> None:
        self.__Width = width
        self.__Height = height
        self.__RenderCommandList = RenderCommandList()

        RenderCommands.INIT()

    def Resize(self, width: float, height: float) -> None:
        self.__RenderCommandList.AddCommand(RenderCommands.Resize, width, height)

    def Render(self, scene: Scene) -> None:
        self.__RenderCommandList.AddCommand(RenderCommands.Clear, 0.1, 0.1, 0.1)
        self.__RenderCommandList.Execute()
