from Utility import *
from Asura.Events import *

def test_Events():
    e = Event()
    assert e.Handled == False

def test_KeyEvents():
    e = KeyEvent(69)
    assert e.KeyCode == 69
    assert e.IsInCategory(EventCategory.Keyboard | EventCategory.Input) == True

    e = KeyPressedEvent(69, 5)
    assert e.EventType == EventType.KeyPressed
    assert e.RepeatCount == 5

    e = CharInputEvent('x')
    assert e.Char == 'x'
    assert e.EventType == EventType.CharInput

    e = KeyReleasedEvent(69)
    assert e.EventType == EventType.KeyReleased

def test_ApplicationEvents():
    e = ApplicationEvent()
    assert e.IsInCategory(EventCategory.Application) == True

    e = WindowResizeEvent(69, 6969)
    assert e.EventType == EventType.WindowResize
    assert (e.Width, e.Height) == (69, 6969)

    e = WindowCloseEvent()
    assert e.EventType == EventType.WindowClose

    e = WindowFocusEvent()
    assert e.EventType == EventType.WindowFocus

    e = WindowMovedEvent(696, 69696)
    assert e.EventType == EventType.WindowMoved
    assert (e.offsetX, e.offsetY) == (696, 69696)

    e = AppTickEvent()
    assert e.EventType == EventType.AppTick
    assert e.Ticks == 1

    e = AppUpdateEvent()
    assert e.EventType == EventType.AppUpdate
    e = AppRenderEvent()
    assert e.EventType == EventType.AppRender

def test_MouseEvents():
    e = MouseEvent()
    assert e.IsInCategory(EventCategory.Mouse | EventCategory.Input) == True

    e = MouseButtonPressedEvent(69)
    assert e.EventType == EventType.MouseButtonPressed
    assert e.ButtonCode == 69
    assert e.IsInCategory(EventCategory.Mouse | EventCategory.Input | EventCategory.MouseButton) == True

    e = MouseButtonReleasedEvent(69)
    assert e.EventType == EventType.MouseButtonReleased
    assert e.ButtonCode == 69
    assert e.IsInCategory(EventCategory.Mouse | EventCategory.Input | EventCategory.MouseButton) == True

    e = MouseMovedEvent(6, 9)
    assert e.EventType == EventType.MouseMoved
    assert (e.OffsetX, e.OffsetY) == (6, 9)
    
    e = MouseScrolledEvent(9, 6)    # OffsetY is supplied first
    assert e.EventType == EventType.MouseScrolled
    assert (e.OffsetY, e.OffsetX) == (9, 6)
