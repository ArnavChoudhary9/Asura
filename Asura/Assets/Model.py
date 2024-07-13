from ..Logging import ClientLoggers

from typing import List
from pyrr import Vector3
from abc import ABC, abstractmethod
from pathlib import Path
from pywavefront import Wavefront

class Model:
    __Vertices: List[Vector3]
    __Indices: List[int]

    def __init__(self) -> None:
        self.__Vertices = []
        self.__Indices = []

    @property
    def Vertices(self) -> List[Vector3]: return self.__Vertices
    @property
    def Indices(self) -> List[int]: return self.__Indices

    def AddVertex(self, vertex: Vector3) -> None: self.__Vertices.append(vertex)
    def AddIndices(self, index: int) -> None: self.__Indices.append(index)

class ModelLoader(ABC):
    @staticmethod
    def LoadModel(path: Path, loader) -> Model: return loader.Load(path)

    @staticmethod
    @abstractmethod
    def Load(path: Path) -> Model: ...

class OBJLoader:
    @staticmethod
    def Load(path: Path) -> Model:
        model = Model()

        try:
            scene = Wavefront(path, collect_faces=True)
            for name, mesh in scene.meshes.items():
                for vertex in mesh.vertices: model.AddVertex(vertex)
                for face in mesh.faces: model.AddIndices(face)
        
        except Exception as e: ClientLoggers.Error("Failed to load OBJ file: {}", path)

        return model
    
def LoadModel(path: Path) -> Model:
    if path.suffix == '.obj': return ModelLoader.LoadModel(path, OBJLoader)
    return Model()
