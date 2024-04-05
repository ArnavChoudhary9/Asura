from .Event       import *
from .Application import *
from .KeyEvent    import *
from .MouseEvent  import *

ASURA_EVENTSYSTEM_VERSION: tuple = (1,0,0)
ASURA_EVENTSYSTEM_VERSION_STR: str = ".".join(
    [str(s) for s in ASURA_EVENTSYSTEM_VERSION]
)

def PrintEventSystem() -> None:
    print("Event-System Online\nVersion: {}".format(ASURA_EVENTSYSTEM_VERSION_STR))
    print("-"*50)
