import bpy
import hpms_data
import hpms_shared

bl_info = {
    "name": "HPMS Tools",
    "description": "Tools collection for HPMS maps.",
    "author": "Ray1184",
    "version": (1, 0),
    "location": "Object Properties",
    "blender": (2, 80, 0),
    "category": "Object",
    "wiki_url": "https://github.com/Ray1184/HPMSPlugin",
    "tracker_url": "https://github.com/Ray1184/HPMSPlugin",
}

classes = (
    hpms_data.HPMSListItem,
    hpms_data.HPMSRoomListAdd,
    hpms_data.HPMSRoomListRemove,
    hpms_data.HPMSRoomList,
    hpms_data.HPMSRoomDropdownOperator,
    hpms_data.HPMSCameraDropdownOperator,
    hpms_data.HPMSDataPanel
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.hpms_room_list = bpy.props.CollectionProperty(type=hpms_data.HPMSListItem)
    bpy.types.Scene.list_index = bpy.props.IntProperty(name="Index for hpms_room_list", default=0)
    bpy.types.Scene.hpms_shared = hpms_shared.HPMSShared()


def unregister():
    del bpy.types.Scene.hpms_shared
    del bpy.types.Scene.list_index
    del bpy.types.Scene.hpms_room_list

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
