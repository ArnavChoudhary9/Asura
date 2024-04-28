from ..Utility import UUID, UUID3Generator, UUID4Generator, MutableSet
from .Entity import Entity
from .Components import *

import esper

class Scene:
    __Name: str
    __UUID: UUID

    __EntityRegistry: esper.World

    __ToDelete: MutableSet[Entity]

    def __init__(self, name: str) -> None:
        self.__Name = name
        self.__UUID = UUID3Generator(name)

        self.__EntityRegistry = esper.World()

        self.__ToDelete = set()

    @property
    def Name(self) -> str: return self.__Name
    @property
    def SceneUUID(self) -> UUID: return self.__UUID
    @property
    def EntityRegistry(self) -> esper.World: return self.__EntityRegistry

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
        newEntity.AddComponent(IDComponent, None, UUID4Generator())

        for component in entity.AllComponents:
            if isinstance(component, IDComponent): continue
            newEntity.AddComponentInstance(component)

        return newEntity
    
    def DestroyEntity(self, entity: Entity) -> None: self.__ToDelete.add(entity)

    def OnUpdate(self) -> None:
        for entity in self.__ToDelete:  
            self.__EntityRegistry.delete_entity(entity.EntityHandle, immediate=True)
        self.__ToDelete.clear()

    def OnUpdateEditor(self, dt: float) -> None:
        self.OnUpdate()

    def OnUpdateRuntime(self, dt: float) -> None:
        self.OnUpdate()

    def OnComponentAdded   (self, entity: Entity, component: CTV) -> None: ...
    def OnComponentRemoved (self, entity: Entity, component: CTV) -> None: ...
