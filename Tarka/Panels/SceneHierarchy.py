from .Panel import *

from Asura import *

class ComponentDrawer:
    @staticmethod
    def Transform(entity: Entity, component: TransformComponent) -> None:
        changedT, newT = GUILibrary.DrawVector3Controls(
            "Transform", component.Translation
        )
        changedR, newR = GUILibrary.DrawVector3Controls(
            "Rotation", component.Rotation,
            resetValues = pyrr.Vector3([0.0, 0.0, 0.0]), speed = 0.5
        )
        changedS, newS = GUILibrary.DrawVector3Controls(
            "Scale", component.Scale,
            resetValues = pyrr.Vector3([1.0, 1.0, 1.0])
        )

        if changedT or changedR or changedS:
            component.SetTranslation(newT)
            component.SetRotation(newR)
            component.SetScale(newS)

    @staticmethod
    def Mesh(entity: Entity, component: MeshComponent) -> None:
        pass

class SceneHierarchyPanel(Panel):
    __Context: Scene | None
    __SelectionContext: Entity | None

    __CopiedTransform: TransformComponent | None
    __CopiedComponent: CTV | None # type: ignore

    def __init__(self) -> None:
        self.__Context = None
        self.__SelectionContext = None

        self.__CopiedTransform = None
        self.__CopiedComponent = None

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
                if imgui.begin_menu("Create Entity"):
                    if imgui.menu_item("Empty Entity")[0]: self.__Context.CreateEntity("Empty Entity") # type: ignore
                    imgui.end_menu()

                imgui.end_popup()
                
        with imgui.begin("Properties"):
            if not self.__SelectionContext: return
            self.__DrawComponents(self.__SelectionContext)
    
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

    def __DrawComponents(self, entity: Entity) -> None:
        if entity.HasComponent(TagComponent):
            tag = entity.GetComponent(TagComponent).Tag
            _, entity.GetComponent(TagComponent).Tag = imgui.input_text("##Tag", tag, 256)

            imgui.same_line()
            imgui.push_item_width(-1)

            if imgui.button("Add Component"): imgui.open_popup("AddComponent")

            if imgui.begin_popup("AddComponent"):
                if imgui.begin_menu("Mesh"):
                    if imgui.menu_item("Empty Mesh")[0]: # type: ignore
                        self.__SelectionContext.AddComponent(MeshComponent) # type: ignore
                        imgui.close_current_popup()

                    imgui.end_menu()
                imgui.end_popup()

            imgui.pop_item_width()

            self.DrawComponent( "Transform" , entity , TransformComponent , ComponentDrawer.Transform )
            self.DrawComponent( "Mesh"      , entity , MeshComponent      , ComponentDrawer.Mesh      )

            if (self.__CopiedTransform or self.__CopiedComponent) and \
                imgui.begin_popup_context_window(popup_flags=imgui.POPUP_NO_OPEN_OVER_ITEMS|imgui.POPUP_MOUSE_BUTTON_RIGHT):

                if self.__CopiedTransform and imgui.menu_item("Paste Transform")[0]: # type: ignore
                    transform = entity.GetComponent(TransformComponent)
                    transform.SetTranslation(self.__CopiedTransform.Translation)
                    transform.SetRotation(self.__CopiedTransform.Rotation)
                    transform.SetScale(self.__CopiedTransform.Scale)
                    self.__CopiedTransform = None

                if self.__CopiedComponent and imgui.menu_item("Paste Component")[0]: # type: ignore
                    componentType = type(self.__CopiedComponent) # type: ignore
                    if entity.HasComponent(componentType): entity.RemoveComponent(componentType) # type: ignore
                    entity.AddComponentInstance(self.__CopiedComponent) # type: ignore
                    self.__CopiedComponent = None

                imgui.end_popup()

    def DrawComponent(
        self, name: str, entity: Entity, componentType: Type[CTV], UIFunction: Callable[[Entity, CTV], None]
    ) -> None:
        if not entity.HasComponent(componentType): return
        
        flags  = imgui.TREE_NODE_DEFAULT_OPEN
        flags |= imgui.TREE_NODE_FRAMED
        flags |= imgui.TREE_NODE_SPAN_AVAILABLE_WIDTH
        flags |= imgui.TREE_NODE_ALLOW_ITEM_OVERLAP
        flags |= imgui.TREE_NODE_FRAME_PADDING

        component = entity.GetComponent(componentType)
        contentRegionAvailable = imgui.get_content_region_available()

        imgui.push_style_var(imgui.STYLE_FRAME_PADDING, (4, 4))
        lineHeight = 26
        imgui.separator()
        isOpen = imgui.tree_node(name, flags)
        imgui.pop_style_var()

        imgui.same_line(contentRegionAvailable[0] - lineHeight * 0.5)
        if imgui.button("+", lineHeight, lineHeight): imgui.open_popup("ComponentSettings")

        removeComponent = False
        if imgui.begin_popup("ComponentSettings"):
            if issubclass(componentType, TransformComponent):
                if imgui.menu_item("Reset Transform")[0]: # type: ignore
                    entity.GetComponent(TransformComponent).Reset()

                imgui.separator()
                if imgui.menu_item("Copy Transform")[0]: # type: ignore
                    self.__CopiedTransform = entity.GetComponent(TransformComponent).Copy()

                if self.__CopiedTransform and imgui.menu_item("Paste Transform")[0]: # type: ignore
                    transform = entity.GetComponent(TransformComponent)
                    transform.SetTranslation(self.__CopiedTransform.Translation)
                    transform.SetRotation(self.__CopiedTransform.Rotation)
                    transform.SetScale(self.__CopiedTransform.Scale)
                    self.__CopiedTransform = None

            else:       
                if imgui.menu_item("Remove Component")[0]: removeComponent = True # type: ignore

                imgui.separator()
                if imgui.menu_item("Copy Component")[0]: # type: ignore
                    self.__CopiedComponent = entity.GetComponent(componentType).Copy()

                if self.__CopiedTransform and isinstance(self.__CopiedComponent, componentType) \
                    and imgui.menu_item("Paste Component")[0]:  # type: ignore
                    entity.RemoveComponent(componentType)
                    entity.AddComponentInstance(self.__CopiedComponent) # type: ignore
                    self.__CopiedComponent = None
            
            imgui.end_popup()

        if isOpen:
            UIFunction(entity, component) # type: ignore
            imgui.tree_pop()

        # Note you will be able to paste the component even after the original is deleted
        if removeComponent: entity.RemoveComponent(componentType)
