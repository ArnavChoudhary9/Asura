# This file contains frequently used GUI elements

import imgui

class GUILibrary:
    @staticmethod
    def TooltipIfHovered(tooltip: str|None = None) -> None:
        if tooltip and imgui.is_item_hovered(): # type: ignore
            imgui.begin_tooltip()
            imgui.text(tooltip)
            imgui.end_tooltip()
