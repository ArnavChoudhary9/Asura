from ..Logging import CoreLogger

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
