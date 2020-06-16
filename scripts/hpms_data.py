import bpy


class HPMSDataPanel(bpy.types.Panel):
    """Creates a HPMS Sector Data utils panel in the Object properties window"""
    bl_label = "HPMS Sector Data"
    bl_idname = "object.hpmsdata"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        return context.object.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        if context.object.name.startswith("SG_"):
            self.draw_data(context)
        else:
            layout.label(text="To define an HPMS sector group, object name must starts with 'SG_'")

    def draw_data(self, context):
        obj = context.object
        layout = self.layout
        row = layout.row()
        row.label(text="Sector Group: " + obj.name)
        layout.separator()
        row = layout.row()
        row.label(text="Linked Camera")
        row = layout.row()
        current_room = context.scene.hpms_shared.get_room_by_sector(obj.name)
        current_cam = context.scene.hpms_shared.get_cam_by_sector_and_room(current_room, obj.name)
        row.operator_menu_enum("object.hpmscam", "linked_camera_list", text=current_cam)

        layout.separator()

        row = layout.row()
        row.label(text="Related to Room")
        row = layout.row()
        current_room = context.scene.hpms_shared.get_room_by_sector(obj.name)
        row.operator_menu_enum("object.hpmsroom", "linked_room_list", text=current_room)

        layout.separator()

        row = layout.row()
        row.label(text="Manage Rooms")
        row = layout.row()
        row.template_list("HPMSRoomList", "Related to Room", context.scene, "hpms_room_list", context.scene,
                          "list_index")
        if context.scene.list_index >= 0 and context.scene.hpms_room_list:
            item = context.scene.hpms_room_list[context.scene.list_index]
            row = layout.row()
            row.prop(item, "name")

        row = layout.row()
        row.operator("hpms_room_list.add", text="Add")
        row.operator("hpms_room_list.remove", text="Remove")


class HPMSCameraDropdownOperator(bpy.types.Operator):
    """Assign a camera for this sector group"""
    bl_idname = "object.hpmscam"
    bl_label = "Linked Camera List"

    def all_cameras(self, context):
        items = [(x.name, x.name, x.name, i) for i, x in enumerate(bpy.data.objects) if x.type == 'CAMERA']
        return items

    def update_cameras(self, context):
        pass

    linked_camera_list = bpy.props.EnumProperty(items=all_cameras, name="Linked Camera List", update=update_cameras)

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        current_room = context.scene.hpms_shared.get_room_by_sector(context.object.name)
        context.scene.hpms_shared.put_cam(current_room, context.object.name, str(self.linked_camera_list))
        return {'FINISHED'}


class HPMSRoomDropdownOperator(bpy.types.Operator):
    """Assign a room for this sector group"""
    bl_idname = "object.hpmsroom"
    bl_label = "Linked Room List"

    def all_rooms(self, context):
        items = [(x.name, x.name, x.name, i) for i, x in enumerate(context.scene.hpms_room_list)]
        return items

    def update_rooms(self, context):
        pass

    linked_room_list = bpy.props.EnumProperty(items=all_rooms, name="Linked Room List", update=update_rooms)

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        context.scene.hpms_shared.put_room(context.object.name, str(self.linked_room_list))
        return {'FINISHED'}


class HPMSListItem(bpy.types.PropertyGroup):
    """Group of properties representing an item in the list."""
    name: bpy.props.StringProperty(
        name="Room Name",
        description="Assigned room")


class HPMSRoomList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        custom_icon = 'WORKSPACE'

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name, icon=custom_icon)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text=item.name, icon=custom_icon)


class HPMSRoomListAdd(bpy.types.Operator):
    """Add a new item to the room list."""
    bl_idname = "hpms_room_list.add"
    bl_label = "Add a new room"

    def execute(self, context):
        context.scene.hpms_room_list.add()
        return {'FINISHED'}


class HPMSRoomListRemove(bpy.types.Operator):
    """Remove item from the room list."""
    bl_idname = "hpms_room_list.remove"
    bl_label = "Remove selected room"

    @classmethod
    def poll(cls, context):
        return context.scene.hpms_room_list

    def execute(self, context):
        room_list = context.scene.hpms_room_list
        index = context.scene.list_index
        room_list.remove(index)
        context.scene.list_index = min(max(0, index - 1), len(room_list) - 1)
        return {'FINISHED'}
