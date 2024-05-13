from ..RenderCommands import * 

from OpenGL.GL import glClear, glClearColor, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, glViewport

class OpenGLRenderCommands:
    @staticmethod
    def Clear(*args) -> None:
        if len(args) == 3: glClearColor(*args, 1.0)
        else: glClearColor(*args)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # type: ignore

    @staticmethod
    def Resize(x: int, y: int) -> None: glViewport(0, 0, int(x), int(y))