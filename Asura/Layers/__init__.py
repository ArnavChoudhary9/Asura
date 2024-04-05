from .Layers import *

ASURA_LAYERSYSTEM_VERSION: tuple = (1,0,0)
ASURA_LAYERSYSTEM_VERSION: str = ".".join(
    [str(s) for s in ASURA_LAYERSYSTEM_VERSION]
)

def PrintLayerSystem() -> None:
    print("Layer System Online\nVersion: {}".format(ASURA_LAYERSYSTEM_VERSION))
    print("-"*50)
