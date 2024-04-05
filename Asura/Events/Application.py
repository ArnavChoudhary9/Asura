'''
Contains Events related to the Application and Window
'''

from .Event import Event, EventType, EventCategory

class ApplicationEvent(Event):
    def __init__(self) -> None: pass

    @property
    def CategoryFlags(self) -> int: return EventCategory.Application

class WindowResizeEvent(ApplicationEvent):
    __slots__ = "__Width", "__Height"

    def __init__(self, width: int, height: int) -> None:
        self.__Width = width
        self.__Height = height

    @property
    def Width(self) -> int: return self.__Width
    @property
    def Height(self) -> int: return self.__Height

    @property
    def EventType(self) -> int: return EventType.WindowResize
    def ToString(self) -> str: return "<WindowResizeEvent: {}, {}>".format(self.__Width, self.__Height)

class WindowCloseEvent(ApplicationEvent):
    @property
    def EventType(self) -> int:
        return EventType.WindowClose

    def ToString(self) -> str:
        return "<WindowCloseEvent>"

class WindowFocusEvent(ApplicationEvent):
    @property
    def EventType(self) -> int:
        return EventType.WindowFocus

    def ToString(self) -> str:
        return "<WindowFocusEvent>"  

class WindowMovedEvent(ApplicationEvent):
    __slots__ = "__offsetX", "__offsetY"

    def __init__(self, offsetX: int, offsetY: int) -> None:
        self.__offsetX = offsetX
        self.__offsetY = offsetY

    @property
    def offsetX(self) -> int: return self.__offsetX
    @property
    def offsetY(self) -> int: return self.__offsetY

    @property
    def EventType(self) -> int: return EventType.WindowMoved
    def ToString(self) -> str: return "<WindowMovedEvent: {}, {}>".format(self.__offsetX, self.__offsetY)

class AppTickEvent(ApplicationEvent):
    _Ticks: int = 0

    def __init__(self) -> None: AppTickEvent._Ticks += 1

    @property
    def Ticks(self) -> int: return AppTickEvent._Ticks

    @property
    def EventType(self) -> int: return EventType.AppTick
    def ToString(self) -> str: return "<AppTickEvent> Ticks: {}".format(AppTickEvent._Ticks)  

class AppUpdateEvent(ApplicationEvent):
    @property
    def EventType(self) -> int: return EventType.AppUpdate
    def ToString(self) -> str: return "<AppUpdateEvent>"  

class AppRenderEvent(ApplicationEvent):
    @property
    def EventType(self) -> int: return EventType.AppRender
    def ToString(self) -> str: return "<AppRenderEvent>"  
