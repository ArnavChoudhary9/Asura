# This file is only for type checking purposes.
from typing import Protocol
import esper

class SupportsScene(Protocol):
    @property
    def EntityRegistry(self) -> esper.World: ...

    def OnComponentAdded(self, entity, component) -> None: ...
    def OnComponentRemoved(self, entity, component) -> None: ...
