from typing import Tuple

from typing import TypeVar as _TypeVar
from typing import Type    as _Type

from ..Logging import ClientLoggers
from .SupportsScene import SupportsScene
from .Components import IDComponent, TagComponent, TransformComponent

_C = _TypeVar("_C")

class Entity:
    __EntityHandle: int
    __Scene: SupportsScene

    def __init__(self, entityHandle: int, scene: SupportsScene) -> None:
        self.__Scene = scene
        self.__EntityHandle = entityHandle

    # This is just for deffered deletion/duplication
    def __hash__(self) -> int: return self.__EntityHandle

    @property
    def Scene(self) -> SupportsScene: return self.__Scene
    @property
    def EntityHandle(self) -> int: return self.__EntityHandle

    @property
    def AllComponents(self) -> Tuple[object, ...]:
        return self.__Scene.EntityRegistry.components_for_entity(self.__EntityHandle)
    
    def __int__(self) -> int: return self.__EntityHandle
    def __bool__(self) -> bool: return self.__EntityHandle != None

    def __eq__(self, other) -> bool:
        if not isinstance(other, Entity): return False
        return ((self.__EntityHandle == other.__EntityHandle) and (self.__Scene == other.__Scene))
    def __ne__(self, other) -> bool: return not (self == other)

    def HasComponent(self, componentType: _Type[_C]) -> bool:
        return self.__Scene.EntityRegistry.has_component(self.__EntityHandle, componentType)
    
    def WarnIfHasComponent(self, componentType: _Type[_C]) -> bool:
        if self.HasComponent(componentType):
            ClientLoggers.Error("Entity {} ({}) already has Component of type: {}", self, self.__EntityHandle, componentType)
            return True
        
        return False

    def GetComponent(self, componentType: _Type[_C]) -> _C:
        return self.__Scene.EntityRegistry.component_for_entity(self.__EntityHandle, componentType)

    def AddComponent(self, componentType: _Type[_C], *args, **kwargs) -> _C:
        if self.WarnIfHasComponent(componentType): return self.GetComponent(componentType)
        
        component = componentType(*args, **kwargs)
        self.__Scene.EntityRegistry.add_component(self.__EntityHandle, component)
        self.__Scene.OnComponentAdded(self, component)
        return component
    
    def AddComponentInstance(self, component: object) -> None:
        if self.WarnIfHasComponent(type(component)): return

        self.__Scene.EntityRegistry.add_component(self.__EntityHandle, component)
        self.__Scene.OnComponentAdded(self, component)
    
    def RemoveComponent(self, componentType: _Type[_C]) -> None:
        if not self.HasComponent(componentType):
            ClientLoggers.Error(
                "Enitiy: {} ({}), Does not have component of type: {}",
                self, int(self), componentType
            )
            return
        
        if componentType in [IDComponent, TagComponent, TransformComponent]:
            ClientLoggers.Warn("Trying to remove an Essential Component from an Entity.")
            return

        component = self.GetComponent(componentType)
        self.__Scene.EntityRegistry.remove_component(self.__EntityHandle, componentType)
        self.__Scene.OnComponentRemoved(self, component)
