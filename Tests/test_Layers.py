from Utility import *
from Asura.Layers import *


def test_EventPropogation() -> None:
    class TestLayer(Layer):
        def OnInitialize(self) -> None:
            self._EventDispatcher.AddHandler(EventType.Null, self.NullEventHandler)

        def NullEventHandler(self, event) -> bool:
            assert False # The event should not reach here
        
        def OnStart(self) -> None: assert True
        def OnUpdate(self, dt: float) -> None: assert dt == 69.69
        def OnStop(self) -> None: assert True

        def OnDestroy(self) -> None: pass

    class TestOverlay(Overlay):
        def OnInitialize(self) -> None:
            self._EventDispatcher.AddHandler(EventType.Null, self.NullEventHandler)

        def NullEventHandler(self, event) -> bool:
            return False

        # These must be defined as the parent class is ABC
        def OnStart(self) -> None: pass
        def OnUpdate(self, _: float) -> None: pass
        def OnStop(self) -> None: pass

        def OnDestroy(self) -> None: pass
        ###################################################
        
        def OnGUIStart(self) -> None: assert True
        def OnGUIRender(self) -> None: assert True
        def OnGUIEnd(self) -> None: assert True

    class TestOverlay2(Overlay):
        def OnInitialize(self) -> None:
            self._EventDispatcher.AddHandler(EventType.Null, self.NullEventHandler)

        def NullEventHandler(self, event) -> bool:
            assert True # The event is handled here
            return True

        # These must be defined as the parent class is ABC
        def OnStart(self) -> None: pass
        def OnUpdate(self, _: float) -> None: pass
        def OnStop(self) -> None: pass

        def OnDestroy(self) -> None: pass
        ###################################################
        
        def OnGUIStart(self) -> None: assert True
        def OnGUIRender(self) -> None: assert True
        def OnGUIEnd(self) -> None: assert True

    stack = LayerStack()
    stack.AddLayer(TestLayer())
    stack.AddOverlay(TestOverlay()) # TestOverlay is added later but it should be first in the stack.
    stack.AddOverlay(TestOverlay2())

    stack.OnEvent(Event())

    stack.OnStart()
    stack.OnUpdate(69.69)
    stack.OnStop()

    stack.OnGUIStart()
    stack.OnGUIRender()
    stack.OnGUIEnd()
