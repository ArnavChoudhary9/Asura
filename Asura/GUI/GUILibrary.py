# This file contains frequently used GUI elements.
# This module is completly separated from the engine and does not use any other modules from the engine.

from typing import Tuple
import imgui
import pyrr

class GUILibrary:
    @staticmethod
    def TooltipIfHovered(tooltip: str|None = None) -> None:
        if tooltip and imgui.is_item_hovered(): # type: ignore
            imgui.begin_tooltip()
            imgui.text(tooltip)
            imgui.end_tooltip()

    @staticmethod
    def DrawVector3Controls(
        lable: str, values: pyrr.Vector3,
        resetValues: pyrr.Vector3 = pyrr.Vector3([0.0, 0.0, 0.0]),
        speed: float = 0.05, columnWidth: float = 100
    ) -> Tuple[bool, pyrr.Vector3]:
        imgui.push_id(lable)

        imgui.columns(2)
        imgui.set_column_width(0, columnWidth)
        imgui.text(lable)
        imgui.next_column()

        imgui.push_item_width(imgui.calculate_item_width()/3)
        imgui.push_item_width(imgui.calculate_item_width()/2.5*2)
        imgui.push_item_width(imgui.calculate_item_width())

        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, imgui.Vec2(0, 1)) # type: ignore
        lineHeight = 23

        imgui.push_style_color( imgui.COLOR_BUTTON         , *(0.80, 0.10, 0.15, 1.00) ) # type: ignore
        imgui.push_style_color( imgui.COLOR_BUTTON_HOVERED , *(0.90, 0.20, 0.20, 1.00) ) # type: ignore
        imgui.push_style_color( imgui.COLOR_BUTTON_ACTIVE  , *(0.80, 0.10, 0.15, 1.00) ) # type: ignore
        if imgui.button("X", lineHeight+3, lineHeight): values.x = resetValues.x
        imgui.pop_style_color(3)

        imgui.same_line()
        xHasChanged, newX = imgui.drag_float("##X", values.x, speed, 0.0, 0.0, format="%.2f") # type: ignore
        imgui.pop_item_width()
        imgui.same_line()

        imgui.push_style_color( imgui.COLOR_BUTTON         , *(0.20, 0.70, 0.20, 1.00) ) # type: ignore
        imgui.push_style_color( imgui.COLOR_BUTTON_HOVERED , *(0.20, 0.80, 0.30, 1.00) ) # type: ignore
        imgui.push_style_color( imgui.COLOR_BUTTON_ACTIVE  , *(0.20, 0.20, 0.20, 1.00) ) # type: ignore
        if imgui.button("Y", lineHeight+3, lineHeight): values.y = resetValues.y
        imgui.pop_style_color(3)

        imgui.same_line()
        yHasChanged, newY = imgui.drag_float("##Y", values.y, speed, 0.0, 0.0, format="%.2f") # type: ignore
        imgui.pop_item_width()
        imgui.same_line()

        imgui.push_style_color( imgui.COLOR_BUTTON         , *(0.10, 0.25, 0.80, 1.00) ) # type: ignore
        imgui.push_style_color( imgui.COLOR_BUTTON_HOVERED , *(0.20, 0.35, 0.90, 1.00) ) # type: ignore
        imgui.push_style_color( imgui.COLOR_BUTTON_ACTIVE  , *(0.10, 0.25, 0.80, 1.00) ) # type: ignore
        if imgui.button("Z", lineHeight+3, lineHeight): values.z = resetValues.z
        imgui.pop_style_color(3)

        imgui.same_line()
        zHasChanged, newZ = imgui.drag_float("##Z", values.z, speed, 0.0, 0.0, format="%.2f") # type: ignore
        imgui.pop_item_width()

        imgui.pop_style_var()
        imgui.columns(1)
        imgui.pop_id()

        return (xHasChanged or yHasChanged or zHasChanged), pyrr.Vector3([ newX, newY, newZ ])
