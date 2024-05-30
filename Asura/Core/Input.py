from .ButtonCodes import *

import glfw
from typing import Tuple

class Input:
    __NativeWindow: int

    @staticmethod
    def Init(nativeWindowHandle) -> None: Input.__NativeWindow = nativeWindowHandle

    @staticmethod
    def IsKeyPressed(keyCode: int) -> bool:
        state = glfw.get_key(Input.__NativeWindow, KeyCodes.ToGLFW(keyCode))
        return (state == glfw.PRESS or state == glfw.REPEAT)
    
    @staticmethod
    def IsMouseButtonPressed(button: int) -> bool:
        return (glfw.get_mouse_button(Input.__NativeWindow, MouseCodes.ToGLFW(button)))
    
    @staticmethod
    def GetMousePosition() -> Tuple[float, float]: return glfw.get_cursor_pos(Input.__NativeWindow)
    @staticmethod
    def GetMouseX() -> float: return Input.GetMousePosition()[0]
    @staticmethod
    def GetMouseY() -> float: return Input.GetMousePosition()[1]
