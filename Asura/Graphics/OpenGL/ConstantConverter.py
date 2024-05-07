from ...Utility.Constants import *

from typing import Dict
from OpenGL.GL import GL_RGB, GL_RGBA, GL_RED_INTEGER, GL_DEPTH24_STENCIL8, \
    GL_RGB8, GL_RGB16, GL_RGBA8, GL_RGBA16, GL_DEPTH_STENCIL, GL_R32I, \
    GL_UNSIGNED_BYTE, GL_UNSIGNED_INT_24_8, \
    GL_REPEAT, GL_MIRRORED_REPEAT, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_BORDER, \
    GL_LINEAR, GL_NEAREST, GL_LINEAR_MIPMAP_LINEAR

_ConversionTable: Dict[int, int] = {
    TextureConstants.Format.RGB: GL_RGB,
    TextureConstants.Format.RGBA: GL_RGBA,
    TextureConstants.Format.RED_INTEGER: GL_RED_INTEGER,
    TextureConstants.Format.DEPTH_STENCIL: GL_DEPTH_STENCIL,

    TextureConstants.Size.RGB8: GL_RGB8,
    TextureConstants.Size.RGB16: GL_RGB16,
    TextureConstants.Size.RGBA8: GL_RGBA8,
    TextureConstants.Size.RGBA16: GL_RGBA16,
    TextureConstants.Size.DEPTH24STENCIL8: GL_DEPTH24_STENCIL8,
    TextureConstants.Size.R32I: GL_R32I,

    TextureConstants.DataType.UNSIGNED_BYTE: GL_UNSIGNED_BYTE,
    TextureConstants.DataType.UNSIGNED_INT_24_8: GL_UNSIGNED_INT_24_8,

    TextureConstants.WrapMode.REPEAT: GL_REPEAT,
    TextureConstants.WrapMode.MIRRORED_REPEAT: GL_MIRRORED_REPEAT,
    TextureConstants.WrapMode.CLAMP_TO_EDGE: GL_CLAMP_TO_EDGE,
    TextureConstants.WrapMode.CLAMP_TO_BORDER: GL_CLAMP_TO_BORDER,

    TextureConstants.Filter.LINEAR: GL_LINEAR,
    TextureConstants.Filter.NEAREST: GL_NEAREST,
    TextureConstants.Filter.MIPMAP_LINEAR: GL_LINEAR_MIPMAP_LINEAR
}

def ConvertConstant(const: int) -> int: return _ConversionTable[const]
