import bpy


def export_room_data(output_path, room_list, update_all, do_render, preview):
    import hpms_utils
    scripts_path = output_path + "/data/scripts"
    maps_path = output_path + "/data/maps"
    screens_path = output_path + "/data/screens"
    depth_path = output_path + "/data/masks"
    rooms = bpy.context.scene.hpms_room_list
    import hpms_lua
    import hpms_maps
    import hpms_render
    for cam in bpy.data.cameras:
        hpms_render.config_cam(cam)
    if do_render:
        hpms_render.configure_renderer(preview)
        import os
        if not os.path.isdir(hpms_utils.get_current_dir() + "/../syslogs"):
            os.mkdir(hpms_utils.get_current_dir() + "/../syslogs")
        open(hpms_utils.get_current_dir() + "/../syslogs/blender_render.log", "w+")
        open(hpms_utils.get_current_dir() + "/../syslogs/blender_export.log", "w+")

    for room in rooms:
        room_name = str(room.name)
        if room_name.rstrip() == "":
            hpms_utils.warn("Found a room with no name, skipping to next")
            continue
        hpms_lua.create_or_update_room_script(scripts_path, room_name, room_list, update_all)

        import hpms_filters
        sectors = hpms_filters.filter_sectors(room_name)

        hpms_maps.create_or_update_room_map(maps_path, room_name, sectors, room_list, update_all)
        if do_render:
            hpms_render.create_or_update_screens(screens_path, depth_path, room_name, room_list, update_all)
