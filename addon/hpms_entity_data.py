import bpy


class HPMSEntityDataPanel(bpy.types.Panel):
    """Creates a HPMS Entity Data utils panel in the Object properties window"""
    bl_label = "HPMS Entity Data"
    bl_idname = "object.hpmsentitydata"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        return context.object.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        if context.object.name.startswith("EM_"):
            self.draw_data(context)
        else:
            layout.label(text="To define an HPMS entity marker, object name must starts with 'EM_'")

    def draw_data(self, context):

        obj = context.object
        layout = self.layout
        row = layout.row()
        row.label(text="Entity: " + obj.name)

        layout.separator()

        row = layout.row()
        row.label(text="Entity Settings")
        row = layout.row()
        row.prop(context.scene.hpms_entity_scene_prop.player, expand=True)
        row = layout.row()
        row.prop(context.object.hpms_entity_obj_prop.color, expand=True)
        row = layout.row()
        row.prop(context.object.hpms_entity_obj_prop.depth, expand=True)
        row = layout.row()
        row.prop(context.object.hpms_entity_obj_prop.animated, expand=True)

        if context.object.hpms_entity_obj_prop.animated:
            self.draw_animation_config(context, layout)

    def draw_animation_config(self, context, layout):
        layout.separator()
        row = layout.row()
        row.label(text="Manage Animations")
        row = layout.row()
        row.template_list("HPMSEntityAnimationConfigList", "Animation configuration", context.object,
                          "hpms_anim_config_list", context.object,
                          "list_index")
        if context.object.list_index >= 0 and context.object.hpms_anim_config_list:
            item = context.object.hpms_anim_config_list[context.object.list_index]
            row = layout.row()
            row.prop(item, "name")
            row.prop(item, "start")
            row.prop(item, "end")
        row = layout.row()
        row.operator("hpms_anim_config_list.add", text="Add")
        row.operator("hpms_anim_config_list.remove", text="Remove")


class HPMSEntitySceneProperties(bpy.types.PropertyGroup):
    """Group of properties representing an entity configuration (scene dependent)."""
    player: bpy.props.BoolProperty(
        name="Player Entity",
        description="Toggle for mark this entity as main player")


class HPMSEntityObjectProperties(bpy.types.PropertyGroup):
    """Group of properties representing an entity configuration (object dependent)."""
    color: bpy.props.BoolProperty(
        name="Write Color",
        description="Toggle for render entity on screen")

    depth: bpy.props.BoolProperty(
        name="Write Depth",
        description="Toggle for render entity depth on depth buffer")

    animated: bpy.props.BoolProperty(
        name="Enable Animation",
        description="")


class HPMSEntityAnimationConfigItem(bpy.types.PropertyGroup):
    """Group of properties representing an animation configuration."""
    name: bpy.props.StringProperty(
        name="Animation Name",
        description="Animation name to play")

    start: bpy.props.IntProperty(
        name="Start Frame",
        description="Frame where animation starts")

    end: bpy.props.IntProperty(
        name="End Frame",
        description="Frame where animation ends")


class HPMSEntityAnimationConfigList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        custom_icon = 'BONE_DATA'

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name, icon=custom_icon)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text=item.name, icon=custom_icon)


class HPMSEntityAnimationConfigListAdd(bpy.types.Operator):
    """Add a new item to the anim config list."""
    bl_idname = "hpms_anim_config_list.add"
    bl_label = "Add a new animation config"

    def execute(self, context):
        context.scene.hpms_room_list.add()
        return {'FINISHED'}


class HPMSEntityAnimationConfigListRemove(bpy.types.Operator):
    """Remove item from the anim config list."""
    bl_idname = "hpms_anim_config_list.remove"
    bl_label = "Remove selected animation config"

    @classmethod
    def poll(cls, context):
        return context.object.hpms_anim_config_list

    def execute(self, context):
        anim_list = context.object.hpms_anim_config_list
        index = context.object.list_index
        anim_list.remove(index)
        context.object.list_index = min(max(0, index - 1), len(anim_list) - 1)
        return {'FINISHED'}


classes = (
    HPMSEntityAnimationConfigListAdd,
    HPMSEntityAnimationConfigListRemove,
    HPMSEntityAnimationConfigItem,
    HPMSEntityAnimationConfigList,
    HPMSEntitySceneProperties,
    HPMSEntityObjectProperties,
    HPMSEntityDataPanel
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Object.hpms_anim_config_list = bpy.props.CollectionProperty(type=HPMSEntityAnimationConfigItem)
    bpy.types.Scene.hpms_entity_scene_prop = bpy.props.PointerProperty(type=HPMSEntitySceneProperties)
    bpy.types.Object.hpms_entity_obj_prop = bpy.props.PointerProperty(type=HPMSEntityObjectProperties)


def unregister():
    del bpy.types.Object.hpms_entity_obj_prop
    del bpy.types.Scene.hpms_entity_scene_prop
    del bpy.types.Object.hpms_anim_config_list
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)