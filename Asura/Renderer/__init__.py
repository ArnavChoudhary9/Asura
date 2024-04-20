from .Renderer import *

ASURA_RENDERER_VERSION: tuple = (1,0,0)
ASURA_RENDERER_VERSION_STR: str = ".".join(
    [str(s) for s in ASURA_RENDERER_VERSION]
)

def PrintRenderer() -> None:
    print("Renerer Online\nVersion: {}".format(ASURA_RENDERER_VERSION_STR))
    print("-"*50)
