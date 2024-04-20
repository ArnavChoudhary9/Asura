from .Layers import *

class LayerStack:
    __Stack: List[Overlay | Layer]
    __LayerIndex: int       # This is the index of the first layer in the stack

    @property
    def Overlays(self): return self.__Stack[:self.__LayerIndex]
    @property
    def Layers(self): return self.__Stack[self.__LayerIndex:]

    def __init__(self) -> None:
        self.__Stack = []
        self.__LayerIndex = 0

    def AddOverlay(self, overlay: Overlay) -> None:
        self.__Stack.insert(self.__LayerIndex, overlay)
        self.__LayerIndex += 1

    def AddLayer(self, layer: Overlay | Layer) -> None:
        '''
        It can handle both layers and overlays
        '''
        if isinstance(layer, Overlay):
            self.AddOverlay(layer)
            return

        self.__Stack.append(layer)

    def OnStart(self) -> None:
        for layer in self.__Stack:
            if not layer.Enabled: continue
            layer.OnStart()

    # C003
    def OnUpdate(self, dt: float) -> None:
        for layer in self.__Stack:
            if not layer.Enabled: continue
            layer.OnUpdate(dt)

    # Ending is done in reverse as the layers which began last should end first.
    def OnStop(self) -> None:
        for layer in self.__Stack[::-1]: # Reverses the list
            if not layer.Enabled: continue
            layer.OnStop()

    # Event handling:
    # Returns if event has been handled.
    # Event propogates through Overlays first, and then through Layers,
    # In the order in which they were added.
    def OnEvent(self, event: Event) -> bool:
        for layer in self.__Stack:
            if not layer.Enabled: continue
            if layer.OnEvent(event): return True

        return False

    # Only for Overlays
    def OnGUIStart(self) -> None:
        for overlay in self.Overlays:
            if not overlay.Enabled: continue
            overlay.OnGUIStart() # type: ignore

    def OnGUIRender(self) -> None:
        for overlay in self.Overlays:
            if not overlay.Enabled: continue
            overlay.OnGUIRender() # type: ignore

    # Ending is done in reverse as the overlays which began last should end first.
    def OnGUIEnd(self) -> None:
        for overlay in self.Overlays[::-1]: # Reverses the list
            if not overlay.Enabled: continue
            overlay.OnGUIEnd() # type: ignore
    # Only for overlays End

    def Destroy(self) -> None:
        # Every layer, no matter enabled or not, will be destroyed
        for layer in self.__Stack: layer.OnDestroy()
