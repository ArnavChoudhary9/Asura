from ..Layers import *
from ..Events import *
from ..Graphics import *
from ..GUI import *
from ..Renderer import *
from ..Utility import perf_counter as CurrentTime
from ..Utility.Constants import AZ_GUI

from ..Instrumentation import *

from abc import ABC, abstractmethod

class AsuraApplication(ABC):
    _Name: str
    _Running: bool
    _LayerStack: LayerStack
    _EventDispatcher: EventDispatcher
    _Window: Window

    # States
    _IsMinimised: bool
    _LastFrameTime: float

    _DeltaTime: float

    def __init__(self, name: str, windowProps: WindowProperties) -> None:
        self._Name = name
        self._Running = True
        self._IsMinimised = False

        self._Window = Window(windowProps)
        self._Window.SetEventCallback(self.OnEvent)

        self._EventDispatcher = EventDispatcher()
        self._EventDispatcher.AddHandler(EventType.WindowClose, self.OnApplicationClose) # type: ignore
        self._EventDispatcher.AddHandler(EventType.WindowResize, self.OnWindowResize) # type: ignore

        self._LayerStack = LayerStack()

        if AZ_GUI:
            self._GUILayer = GUIInitializer(self._Window)
            self._LayerStack.AddOverlay(self._GUILayer)

        self._LastFrameTime = 0.0
        self._DeltaTime = 0.0

    @property
    def Name(self) -> str: return self._Name
    @property
    def DeltaTime(self) -> float: return self._DeltaTime

    @abstractmethod
    # The user Application must overide this method with code they want to run in application loop.
    # C003
    def OnUpdate(self, dt: float) -> None: ...

    def OnEvent(self, event: Event) -> None:
        InstrumentorObj.WriteEvent(event)

        if self._EventDispatcher.Dispatch(event): return

        # If the event handler of application has not handled this event propogate it to layer stack
        self._LayerStack.OnEvent(event)

    def Run(self) -> None:
        runtimeTimer = Timer("Application::Runtime")

        while self._Running:
            updateTimer = Timer("Application::Update")
            _time = CurrentTime()
            self._DeltaTime = _time - self._LastFrameTime
            self._LastFrameTime = _time

            if not self._IsMinimised:
                self._LayerStack.OnUpdate(self._DeltaTime)

                userTimer = Timer("Application::User::OnUpdate")
                self.OnUpdate(self._DeltaTime)
                userTimer.Stop()

                if AZ_GUI:
                    guiUpdateTimer = Timer("Application::GUIUpdate")
                    self._LayerStack.OnGUIStart()
                    self._LayerStack.OnGUIRender()
                    self._LayerStack.OnGUIEnd()
                    guiUpdateTimer.Stop()
            
            self._Window.OnUpdate(self._DeltaTime)
            updateTimer.Stop()

    def OnApplicationClose(self, event: WindowCloseEvent) -> bool:
        ClientLoggers.Trace("OnWindowClose Event receved, closing application!")
        self.Close()
        event.Handled = True
        return True
    
    def OnWindowResize(self, event: WindowResizeEvent) -> bool:
        '''Resizes the window'''

        if event.Width == 0 or event.Height == 0:
            self._IsMinimised = True
            return False

        self._IsMinimised = False
        return False
    
    def Close(self) -> None:
        if not self._Running: return
        self._Running = False

# The user should override this
CreateApplication: Callable[[], AsuraApplication]

def AppRunner() -> None:
    InstrumentorObj.BeginSession("Asura_Initialization")
    app: AsuraApplication = CreateApplication() # type: ignore
    InstrumentorObj.EndSession()

    InstrumentorObj.BeginSession("Asura_Runtime")
    app.Run()
    InstrumentorObj.EndSession()

def Main() -> None:
    if not AZ_INSTRUMENTATION:
        AppRunner()
        return
    
    # Code will enter here if INSTRUMENTATION is enabled
    # This will do some in-depth instrumentation of every function call made
    import cProfile
    import pstats

    with cProfile.Profile() as pr: AppRunner()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename="DetailedProfile.prof")
