from ..Utility import *

from .ButtonCodes import *
from .Input import *

ASURA_VERSION: tuple = (0,3,0,"dev")
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
