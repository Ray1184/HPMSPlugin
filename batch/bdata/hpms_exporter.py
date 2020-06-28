import shutil

import bpy


def backup(output_path, folder):
    scripts_path = output_path + "/data/" + folder
    bak_scripts_path = output_path + "/data/" + folder + "_bak"

    shutil.make_archive(bak_scripts_path, 'zip', scripts_path)


def filter_sectors(room_name):
    sectors = [sec for sec in bpy.data.objects if room_name == sec.hpms_current_room]
    return sectors


def export_room_data(output_path, room_list, update_all, do_render):
    scripts_path = output_path + "/data/scripts"
    maps_path = output_path + "/data/maps"
    backup(output_path, "scripts")
    backup(output_path, "maps")
    rooms = bpy.context.scene.hpms_room_list
    import hpms_lua
    import hpms_maps
    for room in rooms:
        room_name = str(room.name)
        hpms_lua.create_or_update_room_script(scripts_path, room_name, room_list, update_all)
        sectors = filter_sectors(room_name)
        hpms_maps.create_or_update_room_map(maps_path, room_name, sectors, room_list, update_all)
