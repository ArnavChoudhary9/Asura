from .Layers     import *
from .LayerStack import *

ASURA_LAYERSYSTEM_VERSION: tuple = (1,1,0)
ASURA_LAYERSYSTEM_VERSION_STR: str = ".".join(
    [str(s) for s in ASURA_LAYERSYSTEM_VERSION]
)

def PrintLayerSystem() -> None:
    print("Layer System Online\nVersion: {}".format(ASURA_LAYERSYSTEM_VERSION_STR))
    print("-"*50)
