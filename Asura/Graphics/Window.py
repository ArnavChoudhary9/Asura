from ..Core import ASURA_VERSION_STR
from ..Utility import DataClass, Callable, AZ_DEBUG, AZ_CONFIG_STR, AZ_VSYNC, Tuple
from ..Events  import *
from ..Logging import CoreLogger
from .GraphicsContext import GraphicsContext, SuppurtsGraphicsContext

import glfw

@DataClass
class WindowProperties:
    Title: str
    Width: int = 640
    Height: int = 360
    VSync: bool = AZ_VSYNC

    EventCallback: Callable[[Event], None] = lambda _: None # C005

    @property
    def Dimensions(self) -> Tuple[float, float]: return (self.Width, self.Height)

class Window:
    GLFWInitialized: bool = False

    __NativeHandle: int
    __Properties: WindowProperties
    __Context: SuppurtsGraphicsContext

    def __init__(self, properties: WindowProperties) -> None:
        self.__Properties = properties
        CoreLogger.Info("Creating Window: {} ({}x{})", properties.Title, properties.Width, properties.Height)

        if not Window.GLFWInitialized:
            assert glfw.init(), CoreLogger.Critical("Can not intialize GLFW!")

            glfw.set_error_callback(Window.GLFWErrorEventHandler)

            Window.GLFWInitialized = True

        title: str = "{} - PI v{}".format(properties.Title, ASURA_VERSION_STR)
        if AZ_DEBUG: title += " - Config: {}".format(AZ_CONFIG_STR)

        self.__NativeHandle = glfw.create_window(properties.Width, properties.Height, title, None, None)

        self.__Context = GraphicsContext.Create(self.__NativeHandle)
        self.__Context.Init()

        glfw.set_window_user_pointer(self.__NativeHandle, self.__Properties)
        self.SetVSync(AZ_VSYNC)

        # Sets GLFW callbacks
        glfw.set_window_size_callback  ( self.__NativeHandle, Window.WindowResizeEventHandler )
        glfw.set_window_close_callback ( self.__NativeHandle, Window.WindowCloseEventHandler  )
        glfw.set_key_callback          ( self.__NativeHandle, Window.KeyEventHandler          )
        glfw.set_char_callback         ( self.__NativeHandle, Window.CharInputHandler         )
        glfw.set_mouse_button_callback ( self.__NativeHandle, Window.MouseButtonEventHandler  )
        glfw.set_scroll_callback       ( self.__NativeHandle, Window.MouseScrollEventHandler  )
        glfw.set_cursor_pos_callback   ( self.__NativeHandle, Window.MouseMovedEventHandler   )

    def __del__(self) -> None:
        glfw.destroy_window(self.__NativeHandle)

    def OnUpdate(self, dt: float) -> None:
        glfw.poll_events()
        self.__Context.SwapBuffers()

    def SetVSync(self, enable: bool) -> None:
        global AZ_VSYNC

        if (enable): glfw.swap_interval(1)
        else: glfw.swap_interval(0)

        self.__Properties.VSync = enable
        AZ_VSYNC = enable

    #----------------------GLFW CALLBACKS----------------------
    @staticmethod
    def GLFWErrorEventHandler(error, description):
        CoreLogger.Error("GLFW Error ({}): {}", error, description)

    @staticmethod
    def WindowResizeEventHandler(window, width, height):
        props: WindowProperties = glfw.get_window_user_pointer(window)

        props.Width = width
        props.Height = height

        event = WindowResizeEvent(width, height)
        props.EventCallback(event)

    @staticmethod
    def WindowCloseEventHandler(window):
        props: WindowProperties = glfw.get_window_user_pointer(window)
        event = WindowCloseEvent()
        props.EventCallback(event)

    @staticmethod
    def KeyEventHandler(window, key, scancode, action, mods):
        props: WindowProperties = glfw.get_window_user_pointer(window)

        if (action == glfw.PRESS):
            event = KeyPressedEvent(key, 0)
            props.EventCallback(event)

        elif (action == glfw.RELEASE):
            event = KeyReleasedEvent(key)
            props.EventCallback(event)

        elif (action == glfw.REPEAT):
            event = KeyPressedEvent(key, 1)
            props.EventCallback(event)

    @staticmethod
    def CharInputHandler(window, char):
        props: WindowProperties = glfw.get_window_user_pointer(window)
        event = CharInputEvent(char)
        props.EventCallback(event)

    @staticmethod
    def MouseButtonEventHandler(window, button, action, mods):
        props: WindowProperties = glfw.get_window_user_pointer(window)

        if (action == glfw.PRESS):
            event = MouseButtonPressedEvent(button)
            props.EventCallback(event)

        elif (action == glfw.RELEASE):
            event = MouseButtonReleasedEvent(button)
            props.EventCallback(event)

    @staticmethod
    def MouseScrollEventHandler(window, xoffset, yoffset):
        props: WindowProperties = glfw.get_window_user_pointer(window)
        event = MouseScrolledEvent(yoffset, xoffset)
        props.EventCallback(event)

    @staticmethod
    def MouseMovedEventHandler(window, xoffset, yoffset):
        props: WindowProperties = glfw.get_window_user_pointer(window)
        event = MouseMovedEvent(xoffset, yoffset)
        props.EventCallback(event)
    #----------------------------------------------------------

    @property
    def Width(self) -> int: return self.__Properties.Width
    @property
    def Height(self) -> int: return self.__Properties.Height
    @property
    def NativeWindow(self) -> int: return self.__NativeHandle

    def SetEventCallback(self, callback: Callable[[Event], None]) -> None:
        self.__Properties.EventCallback = callback
