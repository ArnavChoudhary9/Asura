from Asura import *

from Panels import *

class _SceneStateManager:
    Edit  : int = 0
    Play  : int = 1
    Pause : int = 2
    
    CurrentState: int

    @staticmethod
    def Init() -> None: _SceneStateManager.CurrentState = _SceneStateManager.Edit

    @staticmethod
    def SwitchToEdit() -> None: _SceneStateManager.CurrentState = _SceneStateManager.Edit
    @staticmethod
    def SwitchToPlay() -> None: _SceneStateManager.CurrentState = _SceneStateManager.Play
    @staticmethod
    def SwitchToPause() -> None: _SceneStateManager.CurrentState = _SceneStateManager.Pause

    @staticmethod
    def IsEditing() -> bool: return _SceneStateManager.CurrentState == _SceneStateManager.Edit
    @staticmethod
    def IsPlaying() -> bool: return _SceneStateManager.CurrentState == _SceneStateManager.Play
    @staticmethod
    def IsPaused() -> bool: return _SceneStateManager.CurrentState == _SceneStateManager.Pause

class EditorLayer(Overlay):
    __dt: float

    __AppOnEventFunction: Callable[[Event], None]
    __EventBlockingFunction: Callable[[bool], None]
    __Renderer: Renderer

    __CurrentProject: Project
    __CurrentScene: Scene

    __ViewportBounds: List[ImVec2]
    __ViewportSize: ImVec2

    __ViewportFocused: bool
    __ViewportHovered: bool

    __IsBlocking: bool
    __MousePosition: Tuple[float, float]

    # Task Bar Icons
    __TaskBarPlayIcon    : Texture
    __TaskBarPauseIcon   : Texture
    __TaskBarStopIcon    : Texture
    __TaskBarRestartIcon : Texture
    __TaskBarStepIcon    : Texture

    __Panels: PanelManager

    # This Layer takes the OnEvent Function as argument to interact with the application,
    # and other layers
    def __init__(
        self,
        appOnEventFunc: Callable[[Event], None],
        dimentions: Tuple[int, int],
        eventBlockingFunction: Callable[[bool], None]
    ) -> None:
        super().__init__("EditorLayer")
        self.__AppOnEventFunction = appOnEventFunc
        self.__Renderer = Renderer(*dimentions)
        self.__EventBlockingFunction = eventBlockingFunction

        # This part of code is run after self.OnInitialize(),
        # so self.__Renderer will not be defined to get the dimentions
        self.__ViewportSize = ImVec2(*dimentions)

        _SceneStateManager.Init()

    def OnInitialize(self) -> None:
        self.__dt = 0.00001
        self.__CurrentProject = Project(Path("DefaultProject"), "DefaultProject")
        self.__CurrentScene = self.__CurrentProject.GetScene(0)

        self.__ViewportBounds = [
            ImVec2(0, 0),
            ImVec2(0, 0)
        ]

        self.__ViewportFocused = self.__ViewportHovered = False
        self.__IsBlocking = False
        self.__MousePosition = (0, 0)

        self._EventDispatcher.AddHandler(EventType.MouseMoved, self.OnMouseMove) # type: ignore

        # Task Bar Icons Loading
        self.__TaskBarPlayIcon    = LoadImageAsTexture(Path( "Tarka\\Resources\\Icons\\ViewportTaskbar\\PlayButton.png"    ))
        self.__TaskBarPauseIcon   = LoadImageAsTexture(Path( "Tarka\\Resources\\Icons\\ViewportTaskbar\\PauseButton.png"   ))
        self.__TaskBarStopIcon    = LoadImageAsTexture(Path( "Tarka\\Resources\\Icons\\ViewportTaskbar\\StopButton.png"    ))
        self.__TaskBarRestartIcon = LoadImageAsTexture(Path( "Tarka\\Resources\\Icons\\ViewportTaskbar\\RestartButton.png" ))
        self.__TaskBarStepIcon    = LoadImageAsTexture(Path( "Tarka\\Resources\\Icons\\ViewportTaskbar\\StepButton.png"    ))

        self.__Panels = PanelManager()

        sceneHierarchyPanel = SceneHierarchyPanel()
        sceneHierarchyPanel.SetContext(self.__CurrentScene)
        self.__Panels.Add(sceneHierarchyPanel)

    def OnMouseMove(self, event: MouseMovedEvent) -> None: self.__MousePosition = event.OffsetX, event.OffsetY

    def OnStart(self) -> None: pass

    def OnUpdate(self, dt: float) -> None:
        self.__dt = dt

        if _SceneStateManager.IsEditing() or _SceneStateManager.IsPaused():
            self.__CurrentScene.OnUpdateEditor(dt)
        elif _SceneStateManager.IsPlaying():
            self.__CurrentScene.OnUpdateRuntime(dt)

        rendererTimer = Timer("Application::Layer::Render")
        self.__Renderer.BeginScene(self.__CurrentScene)
        self.__Renderer.Resize(int(self.__ViewportSize[0]), int(self.__ViewportSize[1]))
        self.__Renderer.Render()
        self.__Renderer.EndScene()
        rendererTimer.Stop()

    def OnStop(self) -> None: pass
    def OnDestroy(self) -> None: pass

    def OnGUIStart(self) -> None:
        optFullscreen = True
        dockspaceFlags = imgui.DOCKNODE_NONE

        windowFlags = imgui.WINDOW_MENU_BAR | imgui.WINDOW_NO_DOCKING
        if optFullscreen:
            viewport = imgui.get_main_viewport()
            imgui.set_next_window_position(*viewport.pos)
            imgui.set_next_window_size(*viewport.size)

            imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0.0)
            imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0.0)

            windowFlags |= imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE | \
                imgui.WINDOW_NO_MOVE
            windowFlags |= imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS | imgui.WINDOW_NO_NAV_FOCUS

        if dockspaceFlags & imgui.DOCKNODE_PASSTHRU_CENTRAL_NODE:
            windowFlags |= imgui.WINDOW_NO_BACKGROUND

        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, ImVec2(0.0, 0.0))
        # This begins the dockspace
        imgui.begin("Dockspace", True, windowFlags)
        imgui.pop_style_var()

        if optFullscreen:
            imgui.pop_style_var(2)
        
        io = imgui.get_io()
        if io.config_flags & imgui.CONFIG_DOCKING_ENABLE:
            dockspaceID = imgui.get_id("DockSpace")
            imgui.dockspace(dockspaceID, (0.0, 0.0), dockspaceFlags)
    
    def OnGUIRender(self) -> None:
        self.ShowMenuBar()
        self.ShowViewport()
        self.ShowViewportToolbar()

        self.__Panels.OnGUIRender()

        self.ShowContentBrowser()
        self.ShowConsole()
        self.ShowDebugStats()

    def ShowMenuBar(self) -> None:
        with imgui.begin_menu_bar():
            if imgui.begin_menu("File"):
                if imgui.menu_item("Quit", "Ctrl+Q", False, True)[0]: # type: ignore
                    self.__AppOnEventFunction(WindowCloseEvent())

                imgui.end_menu()

    def ShowViewport(self) -> None:
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, ImVec2(0.0, 0.0))
        with imgui.begin("Viewport"):
            self.__ViewportSize = imgui.get_content_region_available()

            viewportMinRegion = imgui.get_window_content_region_min()
            viewportMaxRegion = imgui.get_window_content_region_max()
            viewportOffset    = imgui.get_window_position()

            self.__ViewportBounds = [
                ImVec2(
                    viewportOffset[0] + viewportMinRegion[0],
                    viewportOffset[1] + viewportMinRegion[1]
                ),
                ImVec2(
                    viewportOffset[0] + viewportMaxRegion[0],
                    viewportOffset[1] + viewportMaxRegion[1]
                )
            ]

            self.__ViewportFocused = imgui.is_window_focused()
            self.__ViewportHovered = imgui.is_window_hovered()

            self.__IsBlocking = not (self.__ViewportFocused or self.__ViewportHovered)
            self.__EventBlockingFunction(self.__IsBlocking)

            texture = self.__Renderer.Framebuffer.GetColorAttachment(0)
            imgui.image(texture.RendererID, *self.__ViewportSize)
        
        imgui.pop_style_var()

    #--------------------- Start Block: Viewport ---------------------
    def __PlayScene(self) -> None:
        # Create a copy of the scene
        self.__CurrentScene.OnStart()
        _SceneStateManager.SwitchToPlay()

    def __PauseScene  (self) -> None: _SceneStateManager.SwitchToPause()
    def __ResumeScene (self) -> None: _SceneStateManager.SwitchToPlay()

    # Just updates the scene once
    def __StepThroughScene(self) -> None: self.__CurrentScene.OnUpdateEditor(1/60)

    def __RestartScene(self) -> None:
        self.__StopScene()
        self.__PlayScene()

    def __StopScene(self) -> None:
        self.__CurrentScene.OnStop()
        _SceneStateManager.SwitchToEdit()

    def __ShowViewportToolbarButtons(self) -> None:
        size = imgui.get_window_height() - 4.0
        
        NumButtons = 0
        if   _SceneStateManager.IsEditing() : NumButtons = 1
        elif _SceneStateManager.IsPlaying() : NumButtons = 3
        elif _SceneStateManager.IsPaused()  : NumButtons = 4

        imgui.set_cursor_pos_x(
            imgui.get_window_content_region_max()[0]*0.5 - NumButtons*size*0.5
        )

        if _SceneStateManager.IsEditing():
            if imgui.image_button(self.__TaskBarPlayIcon.RendererID, size, size): self.__PlayScene()
            GUILibrary.TooltipIfHovered("Play (F5)")
            return

        elif _SceneStateManager.IsPlaying():
            if imgui.image_button(self.__TaskBarPauseIcon.RendererID, size, size): self.__PauseScene()
            GUILibrary.TooltipIfHovered("Pause (F6)")

            imgui.same_line()
            if imgui.image_button(self.__TaskBarStopIcon.RendererID, size, size): self.__StopScene()
            GUILibrary.TooltipIfHovered("Stop (Shift+F5)")

            imgui.same_line()
            if imgui.image_button(self.__TaskBarRestartIcon.RendererID, size, size): self.__RestartScene()
            GUILibrary.TooltipIfHovered("Restart (Shift+Ctrl+F5)")

            return
        
        elif _SceneStateManager.IsPaused():
            if imgui.image_button(self.__TaskBarPlayIcon.RendererID, size, size): self.__ResumeScene()
            GUILibrary.TooltipIfHovered("Resume (F5)")

            imgui.same_line()
            if imgui.image_button(self.__TaskBarStopIcon.RendererID, size, size): self.__StopScene()
            GUILibrary.TooltipIfHovered("Stop (Shift+F5)")

            imgui.same_line()
            if imgui.image_button(self.__TaskBarRestartIcon.RendererID, size, size): self.__RestartScene()
            GUILibrary.TooltipIfHovered("Restart (Shift+Ctrl+F5)")

            imgui.same_line()
            if imgui.image_button(self.__TaskBarStepIcon.RendererID, size, size): self.__StepThroughScene()
            GUILibrary.TooltipIfHovered("Step (F10)")

            return

    def ShowViewportToolbar(self) -> None:
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, ImVec2(0, 2))
        imgui.push_style_var(imgui.STYLE_ITEM_INNER_SPACING, ImVec2(0, 0))
        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, ImVec2(0, 0))
        imgui.push_style_color(imgui.COLOR_BUTTON, 0, 0, 0, 0) # type: ignore

        colors = imgui.get_style().colors
        buttonHovered = colors[imgui.COLOR_BUTTON_HOVERED]
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, buttonHovered.x, buttonHovered.y, buttonHovered.z, 0.5) # type: ignore
        buttonActive = colors[imgui.COLOR_BUTTON_ACTIVE]
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, buttonActive.x, buttonActive.y, buttonActive.z, 0.5) # type: ignore

        flags = imgui.WINDOW_NO_DECORATION | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_SCROLL_WITH_MOUSE

        with imgui.begin("##Taskbar", flags=flags): self.__ShowViewportToolbarButtons()

        imgui.pop_style_color(3)
        imgui.pop_style_var(3)
    #--------------------------- End Block ---------------------------

    def ShowContentBrowser(self) -> None:
        with imgui.begin("Content Browser"):
            pass

    def ShowConsole(self) -> None:
        with imgui.begin("Console", flags=imgui.WINDOW_NO_FOCUS_ON_APPEARING):
            pass

    def ShowDebugStats(self) -> None:
        with imgui.begin("Debug Stats", flags=imgui.WINDOW_NO_FOCUS_ON_APPEARING):
            imgui.text("FPS: {}".format(int(1 / self.__dt)))
            imgui.text("Is blocking: {}".format(self.__IsBlocking))

            if self.__IsBlocking: return

            imgui.text("Relative mouse position: {}, {}".format(
                self.__MousePosition[0] - self.__ViewportBounds[0][0],
                self.__MousePosition[1] - self.__ViewportBounds[0][1]
            ))

    def OnGUIEnd(self) -> None:
        imgui.end() # This ends the dockspace
