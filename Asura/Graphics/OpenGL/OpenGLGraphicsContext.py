from ...Logging import CoreLogger
from ..GraphicsContext import GraphicsContext

from OpenGL.GL import GL_RENDERER, GL_VENDOR, GL_VERSION, glGetString
import glfw

class OpenGLGraphicsContext(GraphicsContext):
    def Init(self) -> None:
        glfw.make_context_current(self._WindowHandle)

        CoreLogger.Info("OpenGL Renderer found!")

        # These Things might not work on every hardware
        try:
            CoreLogger.Info("Info:")
            CoreLogger.Info("\tVendor    : {}", glGetString(GL_VENDOR))
            CoreLogger.Info("\tRenderer  : {}", glGetString(GL_RENDERER))
            CoreLogger.Info("\tVersion   : {}", glGetString(GL_VERSION))

        except: pass

    def SwapBuffers(self) -> None:
        glfw.swap_buffers(self._WindowHandle)
