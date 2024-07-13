from ..Utility import UUID, UUID3Generator, UUID4Generator, MutableSet, List
from .Entity import Entity
from .Components import *

import esper
from typing import Type

class Scene:
    __Name: str
    __UUID: UUID

    __EntityRegistry: esper.World

    __ToDelete: MutableSet[Entity]
    __ToDuplicate: MutableSet[Entity]

    def __init__(self, name: str) -> None:
        self.__Name = name
        self.__UUID = UUID3Generator(name)

        self.__EntityRegistry = esper.World()

        self.__ToDelete = set()
        self.__ToDuplicate = set()

    @property
    def Name(self) -> str: return self.__Name
    @property
    def SceneUUID(self) -> UUID: return self.__UUID
    @property
    def EntityRegistry(self) -> esper.World: return self.__EntityRegistry

    def SetUUID(self, uuid: UUID) -> None: self.__UUID = uuid

    def CreateEntity(self, name: str) -> Entity:
        return self.CreateEntityWithUUID(name, UUID4Generator())

    def CreateEntityWithUUID(self, name: str, uuid: UUID) -> Entity:
        entity = Entity(self.EntityRegistry.create_entity(), self)
        entity.AddComponent(IDComponent, uuid)
        entity.AddComponent(TagComponent, name)
        entity.AddComponent(TransformComponent)
        return entity
    
    def DuplicateEntity(self, entity: Entity) -> Entity:
        newEntity = Entity(self.EntityRegistry.create_entity(), self)
        newEntity.AddComponent(IDComponent, UUID4Generator())

        for component in entity.AllComponents:
            if isinstance(component, IDComponent): continue
            newEntity.AddComponentInstance(component.Copy()) # type: ignore

        return newEntity
    
    def GetEntitysWithComponent(self, component: Type[CTV]) -> List[Entity]:
        return [Entity(entity, self) for (entity, _) in self.__EntityRegistry.get_component(component)]
    
    def DefferedDuplicateEntity(self, entity: Entity) -> None: self.__ToDuplicate.add(entity)    
    def DestroyEntity(self, entity: Entity) -> None: self.__ToDelete.add(entity)
    
    @property
    def Entities(self) -> List[Entity]:
        return [Entity(entity, self) for entity in self.EntityRegistry._entities.keys()]

    def OnStart(self) -> None: pass

    def OnUpdate(self) -> None:
        for entity in self.__ToDelete:  
            self.__EntityRegistry.delete_entity(entity.EntityHandle, immediate=True)
        self.__ToDelete.clear()

        for entity in self.__ToDuplicate: self.DuplicateEntity(entity)
        self.__ToDuplicate.clear()

    def OnStop(self) -> None: pass

    def OnUpdateEditor(self, dt: float) -> None:
        self.OnUpdate()

    def OnUpdateRuntime(self, dt: float) -> None:
        self.OnUpdate()

    def OnComponentAdded   (self, entity: Entity, component: CTV) -> None: ...
    def OnComponentRemoved (self, entity: Entity, component: CTV) -> None: ...
