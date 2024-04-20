from ..RenderCommands import * 

from OpenGL.GL import glClear, glClearColor, GL_COLOR_BUFFER_BIT

class OpenGLRenderCommands:
    @classmethod
    def Clear(cls, *args) -> None:
        if len(args) == 3: glClearColor(*args, 1.0)
        else: glClearColor(*args)

        glClear(GL_COLOR_BUFFER_BIT)