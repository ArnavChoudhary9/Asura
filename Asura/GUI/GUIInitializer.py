from ..Layers import Overlay
from ..Events import *
from ..Graphics import Window

import imgui
from imgui.integrations.glfw import * # type: ignore

class GUIInitializer(Overlay):
    __BlockEvents: bool = False

    def __init__(self, window: Window) -> None:
        super().__init__("GUIInitializer")
        self.__Renderer = GlfwRenderer(window.NativeWindow, False)

    def OnInitialize(self) -> None:
        imgui.create_context()
        io = imgui.get_io()
        self.__IO = io

        io.config_flags |= imgui.CONFIG_NAV_ENABLE_KEYBOARD
        io.config_flags |= imgui.CONFIG_DOCKING_ENABLE
        io.config_flags |= imgui.CONFIG_VIEWPORTS_ENABLE # type: ignore

        fontLocation = ".\\Asura\\InternalAssets\\Fonts\\opensans\\OpenSans-Regular.ttf"
        io.fonts.add_font_from_file_ttf(fontLocation, 18.0)

        imgui.style_colors_dark()

        style = imgui.get_style()
        if io.config_flags & imgui.CONFIG_VIEWPORTS_ENABLE: # type: ignore
            style.window_rounding = 0.0
            bgColor = style.colors[imgui.COLOR_WINDOW_BACKGROUND]
            style.colors[imgui.COLOR_WINDOW_BACKGROUND] = imgui.Vec4( bgColor.x, bgColor.y, bgColor.z, 1.0 ) # type: ignore

        self._EventDispatcher.AddHandler( EventType.KeyPressed    , self.__KeyboardPressCallback    ) # type: ignore
        self._EventDispatcher.AddHandler( EventType.KeyReleased   , self.__KeyboardReleasedCallback ) # type: ignore
        self._EventDispatcher.AddHandler( EventType.CharInput     , self.__CharInputCallback        ) # type: ignore
        self._EventDispatcher.AddHandler( EventType.WindowResize  , self.__WindowResizeCallback     ) # type: ignore
        self._EventDispatcher.AddHandler( EventType.MouseScrolled , self.__MouseScrollCallback      ) # type: ignore

    def OnDestroy(self) -> None:
        self.__Renderer.shutdown()

    def OnStart(self) -> None: pass
    def OnUpdate(self, _: float) -> None: pass
    def OnStop(self) -> None: pass

    #-----------------EVENTS-----------------
    def OnEvent(self, event: Event) -> bool: return self._EventDispatcher.Dispatch(event)        
    def __KeyboardPressCallback    ( self, e: KeyEvent           ) -> bool:
        io = self.__IO

        io.keys_down[e.KeyCode] = True

        if self.__BlockEvents: return True
        return False
    def __KeyboardReleasedCallback ( self, e: KeyEvent           ) -> bool:
        io = self.__IO

        io.keys_down[e.KeyCode] = False

        # io.key_ctrl = (
        #     io.keys_down[ Input.IsKeyPressed(PI_KEY_LEFT_CONTROL) ] or
        #     io.keys_down[ Input.IsKeyPressed(PI_KEY_RIGHT_CONTROL) ]
        # )

        # io.key_alt = (
        #     io.keys_down[ Input.IsKeyPressed(PI_KEY_LEFT_ALT) ] or
        #     io.keys_down[ Input.IsKeyPressed(PI_KEY_RIGHT_ALT) ]
        # )

        # io.key_shift = (
        #     io.keys_down[ Input.IsKeyPressed(PI_KEY_LEFT_SHIFT) ] or
        #     io.keys_down[ Input.IsKeyPressed(PI_KEY_RIGHT_SHIFT) ]
        # )

        # io.key_super = (
        #     io.keys_down[ Input.IsKeyPressed(PI_KEY_LEFT_SUPER) ] or
        #     io.keys_down[ Input.IsKeyPressed(PI_KEY_RIGHT_SUPER) ]
        # )

        if self.__BlockEvents: return True
        return False
    def __CharInputCallback        ( self, e: CharInputEvent     ) -> bool:
        io = self.__IO

        if 0 < e.Char < 0x10000:
            io.add_input_character(e.Char)
            if self.__BlockEvents: return True

        return False
    def __WindowResizeCallback     ( self, e: WindowResizeEvent  ) -> bool:
        self.__IO.display_size = e.Width, e.Height

        if self.__BlockEvents: return True
        return False
    def __MouseScrollCallback      ( self, e: MouseScrolledEvent ) -> bool:
        self.__IO.mouse_wheel_horizontal = e.OffsetX
        self.__IO.mouse_wheel = e.OffsetY
        
        if self.__BlockEvents: return True
        return False
    #----------------------------------------

    def BlockEvents(self, block: bool) -> None: self.__BlockEvents = block

    def OnGUIStart(self) -> None:
        self.__Renderer.process_inputs()
        imgui.new_frame()

    def OnGUIRender(self) -> None: pass

    def OnGUIEnd(self) -> None:
        imgui.render()
        self.__Renderer.render(imgui.get_draw_data())

        io = imgui.get_io()
        if io.config_flags & imgui.CONFIG_VIEWPORTS_ENABLE: # type: ignore
            backupCurrentContext = glfw.get_current_context()
            imgui.update_platform_windows()
            imgui.render_platform_windows_default() # type: ignore
            glfw.make_context_current(backupCurrentContext)

    
