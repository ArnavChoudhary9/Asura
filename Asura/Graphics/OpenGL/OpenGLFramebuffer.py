from ..Framebuffer import *
from .ConstantConverter import ConvertConstant

from OpenGL.GL import glGenFramebuffers, glBindFramebuffer, GL_FRAMEBUFFER, \
    glFramebufferTexture2D, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, GL_RED_INTEGER, \
    GL_DEPTH_STENCIL_ATTACHMENT, glDrawBuffer, GL_NONE, glDrawBuffers, \
    glCheckFramebufferStatus, glReadBuffer, glReadPixels, GL_FRAMEBUFFER_COMPLETE, \
    glClearTexImage, GL_INT, glDeleteFramebuffers


MAX_FRAMEBUFFER_SIZE: int = 8192

class OpenGLFramebuffer(Framebuffer):
    __Specification: FramebufferSpecification
    __Textures: List[Texture]
    __RendererID: int

    __DepthTexture: Texture
    
    def __init__(self, specs: FramebufferSpecification) -> None:
        self.__Specification = specs
        self.__RendererID = 0
        self.Invalidate()
    
    def __del__(self) -> None:
        for texture in self.__Textures: del texture
        glDeleteFramebuffers(1, [self.__RendererID])

    def Invalidate(self) -> None:
        if self.__RendererID:
            glDeleteFramebuffers(1, [self.__RendererID])
            for texture in self.__Textures: del texture
            self.__Textures.clear()

        self.__Textures = []

        self.__RendererID = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.__RendererID)


        numColorBuffers = -1
        numDepthBuffers = -1
        dim = self.__Specification.Dimensions

        for spec in self.__Specification.Attachments:
            texture = Texture2D.Create(*dim, spec)

            if spec.TextureFormat in [
                TextureConstants.Format.RGB, TextureConstants.Format.RGBA,
                TextureConstants.Format.RED_INTEGER
            ]:
                numColorBuffers += 1
                assert numColorBuffers < 4, CoreLogger.Error("There can be atmost 4 color attacment.")

                texture.Bind()
                glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0 + numColorBuffers, GL_TEXTURE_2D, texture.RendererID, 0) # type: ignore
                texture.Unbind()

            elif spec.TextureFormat == TextureConstants.Format.DEPTH_STENCIL:
                numDepthBuffers += 1
                self.__DepthTexture = texture
                assert numDepthBuffers < 1, CoreLogger.Error("There can be atmost 1 depth attacment.")

                texture.Bind()
                glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_TEXTURE_2D, texture.RendererID, 0) # type: ignore
                texture.Unbind()

            self.__Textures.append(texture)

        if numColorBuffers == -1:
            glDrawBuffer(GL_NONE)
        elif numDepthBuffers >= 1:
            glDrawBuffers(
                numColorBuffers,
                [ GL_COLOR_ATTACHMENT0 + index for index in range(numColorBuffers) ] # type: ignore
            )

        assert glCheckFramebufferStatus(GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE, CoreLogger.Error(
            "Framebuffer is incomplete"
        )
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    @property
    def Specifications(self) -> FramebufferSpecification: return self.__Specification

    def Bind(self) -> None: glBindFramebuffer(GL_FRAMEBUFFER, self.__RendererID)
    def Unbind(self) -> None: glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def ClearAttachment(self, index: int, value: bytes) -> None:
        texture = self.__Textures[index]
        _format = ConvertConstant(texture.Specifications.TextureFormat)
        _id = texture.RendererID
        glClearTexImage(
            _id, 0,
            _format, GL_INT, value
        )

    def GetColorAttachment(self, index: int=0) -> Texture: return self.__Textures[index]

    def Resize(self, width: int, height: int) -> None:
        if (width * height) == 0 or width > MAX_FRAMEBUFFER_SIZE or height > MAX_FRAMEBUFFER_SIZE:
            CoreLogger.Warn("Attempting to resize framebuffer to {}x{}", width, height)
            return
        
        self.__Specification.Width = width
        self.__Specification.Height = height

        self.Invalidate()
        
    def ReadPixel(self, index: int, x: int, y: int) -> bytes:
        glReadBuffer(GL_COLOR_ATTACHMENT0 + index) # type: ignore
        return bytes(glReadPixels(x, y, 1, 1, GL_RED_INTEGER, GL_INT))
