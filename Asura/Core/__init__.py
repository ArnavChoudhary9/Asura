from ..Utility import *

ASURA_VERSION: tuple = (0,2,0,"dev")
ASURA_VERSION_STR: str = ".".join(
    [str(s) for s in ASURA_VERSION]
)

if AZ_DEBUG:
    def PrintCore():
        print(
            "-"*50,
            "Core Systems Online",
            "Engine Version: {}".format(ASURA_VERSION_STR),
            "-"*50, sep='\n'
        )
