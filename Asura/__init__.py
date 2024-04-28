from .Application import *
from .Core        import *
from .Events      import *
from .Graphics    import *
from .GUI         import *
from .Layers      import *
from .Logging     import *
from .Project     import *
from .Renderer    import *
from .Scene       import *
from .Utility     import *

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
