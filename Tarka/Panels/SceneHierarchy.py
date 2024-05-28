from .Panel import *

from Asura import *

class SceneHierarchyPanel(Panel):
    __Context: Scene | None
    __SelectionContext: Entity | None

    def __init__(self) -> None:
        self.__Context = None
        self.__SelectionContext = None

    def SetContext(self, context: Scene) -> None: self.__Context = context
    def SetSelectionContext(self, context: Entity) -> None: self.__SelectionContext = context
    @property
    def SelectionContext(self) -> Entity | None: return self.__SelectionContext

    def OnGUIRender(self) -> None:
        if not self.__Context:
            ClientLoggers.Error("You need to set Context before calling OnGUIRender")
            return

        with imgui.begin("Scene Heirarchy"):
            for entity in self.__Context.Entities: self.__DrawEntityNode(entity)
            if imgui.is_mouse_down(0) and imgui.is_window_hovered(): self.__SelectionContext = None

            if imgui.begin_popup_context_window(popup_flags=imgui.POPUP_NO_OPEN_OVER_ITEMS|imgui.POPUP_MOUSE_BUTTON_RIGHT):
                if imgui.menu_item("Create Entity")[0]: self.__Context.CreateEntity("Entity") # type: ignore
                imgui.end_popup()
                
        with imgui.begin("Properties"):
            if not self.__SelectionContext: return
    
    def __DrawEntityNode(self, entity: Entity) -> None:
        if not self.__Context:
            ClientLoggers.Error("You need to set Context before calling OnGUIRender")
            return
        
        tag = entity.GetComponent(TagComponent)

        flags = 0
        if self.__SelectionContext == entity: flags |= imgui.TREE_NODE_SELECTED
        flags |= imgui.TREE_NODE_OPEN_ON_ARROW | imgui.TREE_NODE_SPAN_AVAILABLE_WIDTH

        # Adding this to make each entity unique
        # NOTE: int(entity) retrives its __EntityHandle
        opened = imgui.tree_node(str(tag) + f"##{int(entity)}", flags)
        if imgui.is_item_clicked(): self.__SelectionContext = entity

        if imgui.begin_popup_context_item():
            if imgui.menu_item("Duplicate Entity")[0]: self.__Context.DefferedDuplicateEntity(entity) # type: ignore
            if imgui.menu_item("Delete Entity")[0]: # type: ignore
                self.__Context.DestroyEntity(entity)
                if self.__SelectionContext == entity: self.__SelectionContext = None
            imgui.end_popup()

        if opened: imgui.tree_pop()
