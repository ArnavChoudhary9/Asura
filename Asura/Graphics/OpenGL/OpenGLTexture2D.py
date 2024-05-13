from .ConstantConverter import ConvertConstant

from ..Texture import *
from ...Utility import UUID, UUID4Generator

from OpenGL.GL import glGenTextures, glBindTexture, GL_TEXTURE_2D, glTextureStorage2D, \
    glTextureParameteri, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_TEXTURE_MIN_FILTER, \
    GL_TEXTURE_MAG_FILTER, glDeleteTextures, glTextureSubImage2D, glBindTextureUnit
    

class OpenGLTexture2D(Texture2D):
    __RendererID: int
    __Width: int
    __Height: int
    __Specification: TextureSpecification

    __UUID: UUID

    def __init__(self, width: int, height: int, spec: TextureSpecification) -> None:
        self.__Width = width
        self.__Height = height
        self.__Specification = spec
        self.__UUID = UUID4Generator()

        self.__RendererID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.__RendererID)
        glTextureStorage2D(self.__RendererID, 1, ConvertConstant(spec.TextureSize), width, height)

        glTextureParameteri(self.__RendererID, GL_TEXTURE_WRAP_S, ConvertConstant(spec.WrapS))
        glTextureParameteri(self.__RendererID, GL_TEXTURE_WRAP_T, ConvertConstant(spec.WrapT))

        glTextureParameteri(self.__RendererID, GL_TEXTURE_MIN_FILTER, ConvertConstant(spec.MinFilter))
        glTextureParameteri(self.__RendererID, GL_TEXTURE_MAG_FILTER, ConvertConstant(spec.MagFilter))
        glBindTexture(GL_TEXTURE_2D, 0)

    def __del__(self) -> None:
        if self.__RendererID is None: return
        glDeleteTextures(1, [self.__RendererID])

    @property
    def RendererID(self) -> int: return self.__RendererID
    @property
    def Width(self) -> int: return self.__Width
    @property
    def Height(self) -> int: return self.__Height
    @property
    def Dimension(self) -> Tuple[int, int]: return (self.__Width, self.__Height)
    @property
    def TextureUUID(self) -> UUID: return self.__UUID
    @property
    def Specifications(self) -> TextureSpecification:
        return self.__Specification
    
    def SetData(self, data, size) -> None:
        glTextureSubImage2D(
            self.__RendererID, 0, 0, 0,
            self.__Width, self.__Height,
            ConvertConstant(self.__Specification.TextureFormat),
            ConvertConstant(self.__Specification.DataType), data
        )

    def Bind(self, slot: int=0) -> None: glBindTextureUnit(slot, self.__RendererID)
    def Unbind(self) -> None: glBindTextureUnit(0, 0)
