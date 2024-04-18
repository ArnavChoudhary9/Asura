AZ_DEBUG   : bool = True
AZ_LOGGING : bool = True
AZ_GUI     : bool = True
AZ_INSTRUMENTATION: bool = True

AZ_VSYNC: bool = True
#----------------------------------------------------------------

#----------------------------------------------------------------
AZ_CONFIG = 0
AZ_CONFIG_STR_LIST = [
    "DEBUG",
    "NO_LOGGING",
    "NO_INSTRUMENTATION",
    "RELEASE",
    "RELEASE_NO_GUI"
]
AZ_CONFIG_STR: str = AZ_CONFIG_STR_LIST[AZ_CONFIG]

if AZ_CONFIG == 0:
    AZ_DEBUG   : bool = True
    AZ_LOGGING : bool = True
    AZ_GUI     : bool = True
    AZ_INSTRUMENTATION: bool = True

elif AZ_CONFIG == 1:
    AZ_DEBUG   : bool = True
    AZ_LOGGING : bool = False
    AZ_GUI     : bool = True
    AZ_INSTRUMENTATION: bool = True

elif AZ_CONFIG == 2:
    AZ_DEBUG   : bool = True
    AZ_LOGGING : bool = True
    AZ_GUI     : bool = True
    AZ_INSTRUMENTATION: bool = False

elif AZ_CONFIG == 3:
    AZ_DEBUG   : bool = False
    AZ_LOGGING : bool = False
    AZ_GUI     : bool = True
    AZ_INSTRUMENTATION: bool = False

elif AZ_CONFIG == 4:
    AZ_DEBUG   : bool = False
    AZ_LOGGING : bool = False
    AZ_GUI     : bool = False
    AZ_INSTRUMENTATION: bool = False
#----------------------------------------------------------------

#----------------------------------------------------------------
class GraphicsLibraryENUM:
    Headless : int = 0
    OpenGL   : int = 1

    # Vulkan   : int = 2

AZ_GRAPHICSLIBRARY = GraphicsLibraryENUM.OpenGL
#----------------------------------------------------------------
