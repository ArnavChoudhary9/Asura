from .Utility     import *
from .Core        import *
from .Logging     import *
from .Events      import *
from .Layers      import *
from .Application import *
from .Graphics    import *
from .GUI         import *
from .Renderer    import *

from .Instrumentation import *

import imgui
ImVec2 = imgui.Vec2 # type: ignore
ImVec4 = imgui.Vec4 # type: ignore

def PrintAllModulesNames():
    if AZ_DEBUG:
        PrintCore()
        PrintLogging()
        PrintEventSystem()
        PrintLayerSystem()
        PrintInstrumentationSystem()
        PrintGraphicsEngine()
        PrintRenderer()
