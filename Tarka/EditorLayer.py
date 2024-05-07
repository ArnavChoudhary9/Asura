from Asura import *

class EditorLayer(Overlay):
    dt: float

    __AppOnEventFunction: Callable[[Event], None]
    __Renderer: Renderer

    __CurrentProject: Project
    __CurrentScene: Scene

    # This Layer takes the OnEvent Function as argument to interact with the application,
    # and other layers
    def __init__(self, appOnEventFunc: Callable[[Event], None], renderer: Renderer) -> None:
        super().__init__("EditorLayer")
        self.__AppOnEventFunction = appOnEventFunc
        self.__Renderer = renderer

    def OnInitialize(self) -> None:
        self.dt = 0.00001
        self.__CurrentProject = Project(Path("DefaultProject"), "DefaultProject")
        self.__CurrentScene = self.__CurrentProject.GetScene(0)

    def OnStart(self) -> None: pass

    def OnUpdate(self, dt: float) -> None:
        self.dt = dt

        self.__CurrentScene.OnUpdateEditor(dt)
        self.__Renderer.Render(self.__CurrentScene)

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
        self.ShowSceneHeirarchy()
        self.ShowProperties()
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
        with imgui.begin("Viewport"):
            texture = self.__Renderer.Framebuffer.GetColorAttachment(0)
            imgui.image(texture.RendererID, 640, 360)

    def ShowViewportToolbar(self) -> None:
        with imgui.begin("Viewport Toolbar"):
            pass

    def ShowSceneHeirarchy(self) -> None:
        with imgui.begin("Scene Heirarchy"):
            pass

    def ShowProperties(self) -> None:
        with imgui.begin("Properties"):
            pass

    def ShowContentBrowser(self) -> None:
        with imgui.begin("Content Browser"):
            pass

    def ShowConsole(self) -> None:
        with imgui.begin("Console"):
            pass

    def ShowDebugStats(self) -> None:
        with imgui.begin("Debug Stats"):
            imgui.text("FPS: {}".format(int(1 / self.dt)))

            framebuffer = self.__Renderer.Framebuffer
            framebuffer.Bind()
            value = Math.BytesToPythonInt32(framebuffer.ReadPixel(1, 0, 0))
            framebuffer.Unbind()
            
            imgui.text("Red Integer value: {}".format(value))

    def OnGUIEnd(self) -> None:
        imgui.end() # This ends the dockspace
