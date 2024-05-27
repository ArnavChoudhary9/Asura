from ..Logging import CoreLogger
from ..Graphics.Texture import Texture2D, Texture, TextureSpecification

from PIL import Image as _PILImage
from PIL.Image import Image
from pathlib import Path

def LoadImage(path: Path) -> Image:
    try: image = _PILImage.open(path)
    except FileNotFoundError as e:
        CoreLogger.Error("File: {} Not Found", path)
        raise e
    
    # TODO: Convert to RGB/RGBA/sRGB/sRGBA also.
    return image.convert("RGBA")

def LoadImageAsTexture(path: Path) -> Texture:
    image = LoadImage(path)
    texture = Texture2D.Create(image.width, image.height, TextureSpecification())
    texture.SetData(image.tobytes(), None)
    return texture
