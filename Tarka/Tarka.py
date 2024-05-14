# Hackey Fix for relative path problem
# TODO: Try to remove it later
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Main Code starts from here
from Asura import *
from EditorLayer import *

PrintAllModulesNames()

class Tarka(AsuraApplication):
    def __init__(self) -> None:
        dimentions = 1280, 720
        super().__init__("Tarka", WindowProperties(
            "Tarka",
            *dimentions
        ))

        # This Layer takes the OnEvent Function as argument to interact with the application,
        # and other layers
        self._LayerStack.AddOverlay(EditorLayer(self.OnEvent, dimentions, self._GUILayer.BlockEvents))

    def OnUpdate(self, dt: float) -> None: pass

App.CreateApplication = lambda: Tarka()
Main()
