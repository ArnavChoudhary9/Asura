from .Window import *
from .GraphicsContext import *
from .RenderCommands import *

ASURA_GRAPHICSENGINE_VERSION: tuple = (1,0,0)
ASURA_GRAPHICSENGINE_VERSION_STR: str = ".".join(
    [str(s) for s in ASURA_GRAPHICSENGINE_VERSION]
)

def PrintGraphicsEngine() -> None:
    print("Graphics Engine Online\nVersion: {}".format(ASURA_GRAPHICSENGINE_VERSION_STR))
    print("-"*50)
