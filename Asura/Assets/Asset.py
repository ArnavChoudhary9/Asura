from time import time
from pathlib import Path
from abc import ABC, abstractmethod

class BaseAsset(ABC):
    __FilePath: Path
    __LastAccessed: float

    def __init__(self, filePath: Path) -> None:
        self.__FilePath = filePath
        self.__LastAccessed = time()

    @property
    def Path(self) -> Path: return self.__FilePath
    @property
    def LastAccessed(self) -> float: return self.__LastAccessed

    @abstractmethod
    def Load(self) -> None: ...
    @abstractmethod
    def Unload(self) -> None: ...

    def IsExpired(self, expiryTime: float) -> bool:
        return (time() - self.__LastAccessed) > expiryTime
