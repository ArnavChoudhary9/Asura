from ..Utility import Path, List
from ..Core import ASURA_VERSION_STR

from .Scene import *
from .Entity import *
from .Components import *

import yaml

# Helper class for handling YAML serialization
class AZ_YAML:
    @staticmethod
    def EncodeVector3(dumper: yaml.Dumper, vec: pyrr.Vector3) -> yaml.SequenceNode:
        return dumper.represent_sequence(
            "Vector3",
            [float(vec[0]), float(vec[1]), float(vec[2])],
            flow_style=True
        )
    
    @staticmethod
    def DecodeVector3(loader: yaml.Loader, node: yaml.SequenceNode) -> pyrr.Vector3:
        return pyrr.Vector3(loader.construct_sequence(node))
        
    @staticmethod
    def EncodeVector4(dumper: yaml.Dumper, vector: pyrr.Vector4) -> yaml.SequenceNode:
        return dumper.represent_sequence(
            "Vector4",
            [ float(vector[0]), float(vector[1]), float(vector[2]), float(vector[3]) ],
            flow_style=True
        )

    @staticmethod
    def DecodeVector4(loader: yaml.Loader, node: yaml.SequenceNode) -> pyrr.Vector4:
        return pyrr.Vector4(loader.construct_sequence(node))

class SceneSerializer:
    @staticmethod
    def Serialize(scene: Scene, path: Path) -> None:
        data = {}
        data["Scene"] = scene.Name
        data["UUID"] = str(scene.SceneUUID)
        data["Version"] = ASURA_VERSION_STR

        entities: List[Dict] = []
        registry = scene.EntityRegistry
        for entityID in range(1, registry._next_entity_id+1):
            if not registry.entity_exists(entityID): continue
            entity = Entity(entityID, scene)

            entityDict = {
                "Entity": str(entity.GetComponent(IDComponent))
            }

            for component in entity.AllComponents:
                if isinstance(component, IDComponent): continue
                entityDict.update(component.Serialize()) # type: ignore

            entities.append(entityDict)
            
        data["Entities"] = entities

        yaml.add_representer(pyrr.Vector3, AZ_YAML.EncodeVector3)
        yaml.add_representer(pyrr.Vector4, AZ_YAML.EncodeVector4)
        with path.open('w') as file: yaml.dump(data, file)

        ClientLoggers.Info("Scene {}, saved at path: {}", scene.Name, str(path))

    @staticmethod
    def Deserialize(path: Path) -> Scene:
        scene = Scene("NewScene")
        return scene
