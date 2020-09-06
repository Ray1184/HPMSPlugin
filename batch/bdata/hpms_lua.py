import os
from math import radians

import hpms_utils

INDENT = "    "
START_USER_CODE = "-- BEGIN HERE USER CODE"
END_USER_CODE = "-- END HERE USER CODE"


def get_user_code(path, room_name):
    script = path + "/" + room_name + ".lua"
    with open(script) as f:
        lines = [line.rstrip() for line in f]
    sections = [""] * 5
    sec_id = 0
    acquire = False
    for line in lines:

        if END_USER_CODE in line.upper():
            sec_id += 1
            acquire = False

        if acquire:
            sections[sec_id] += line + "\n"

        if START_USER_CODE in line.upper():
            acquire = True

    return sections


def fill_section(content, from_string, to_string):
    to_string = str(to_string)
    if to_string is None or to_string == "":
        to_string = ""
    else:
        to_string = to_string.rstrip()
    return content.replace(from_string, to_string)


def get_cam_by_name(name, cameras):
    for cam in cameras:
        if name == cam.name:
            return cam


def fill_setup_data(content, room_name):
    import hpms_fncall_templates
    import hpms_filters
    entities = hpms_filters.filter_entities(room_name)
    init_code = INDENT + INDENT + "-- BEGIN AUTO-GENERATED CODE\n"
    init_code += INDENT + INDENT + "common = require(\"data/scripts/Common\")\n\n"
    init_code += INDENT + INDENT + "scene.ambient_light = hpms.vec3(1, 1, 1)\n\n"
    init_code += INDENT + INDENT + fill_section(hpms_fncall_templates.MAKE_FLOOR, "%%ROOM_NAME%%", room_name) + "\n\n"
    for ent in entities:
        ent_name = ent.name
        init_code += INDENT + INDENT + fill_section(hpms_fncall_templates.MAKE_ENTITY, "%%ENT_NAME%%",
                                                    ent_name) + "\n"
        pos = ent.location
        rot = ent.rotation_euler
        scale = ent.scale
        location = fill_section(hpms_fncall_templates.POS_ROT_SCALE, "%%ENT_NAME%%", ent_name)
        location = fill_section(hpms_fncall_templates.ADD_ENTITY, "%%ENT_NAME%%", ent_name)
        location = fill_object_position_rotation(location, pos, rot)
        location = fill_object_scale(location, scale)

        init_code += INDENT + INDENT + location + "\n"

    init_code += "\n"

    cameras = hpms_filters.filter_cameras(room_name)
    for cam in cameras:
        cam_name = cam.name
        init_code += INDENT + INDENT + fill_section(hpms_fncall_templates.MAKE_BACKGROUND, "%%CAM_NAME%%",
                                                    cam_name) + "\n"
        init_code += INDENT + INDENT + fill_section(hpms_fncall_templates.MAKE_DEPTH_MASK, "%%CAM_NAME%%",
                                                    cam_name) + "\n"

    init_code += INDENT + INDENT + "-- END AUTO-GENERATED CODE\n\n"
    return fill_section(content, "%%SETUP_CODE%%", init_code)


def fill_update_data(content, room_name):
    import hpms_fncall_templates
    import hpms_filters
    player = hpms_filters.filter_player(room_name)
    sectors = hpms_filters.filter_sectors(room_name)
    cameras = hpms_filters.filter_cameras(room_name)
    room_sectors = [sec for sec in sectors if sec.hpms_current_room == room_name]
    update_code = INDENT + INDENT + "-- BEGIN AUTO-GENERATED CODE\n"
    for sec in room_sectors:
        sec_name = sec.name
        cam = get_cam_by_name(sec.hpms_current_cam, cameras)
        ent_name = player.name
        pos = cam.location
        rot = cam.rotation_euler
        location = fill_section(hpms_fncall_templates.ON_SECTOR_CHANGE_VIEW, "%%ENT_NAME%%", ent_name)
        location = fill_section(location, "%%SECTOR_NAME%%", sec_name)
        location = fill_section(location, "%%ROOM_NAME%%", room_name)
        location = fill_object_position_rotation(location, pos, rot)
        location = fill_section(location, "%%CAM_NAME%%", sec.hpms_current_cam)
        update_code += INDENT + INDENT + location + "\n"

    update_code += INDENT + INDENT + "-- END AUTO-GENERATED CODE\n\n"
    return fill_section(content, "%%UPDATE_CODE%%", update_code)


def fill_input_data(content):
    import hpms_filters
    input_code = INDENT + INDENT + "-- BEGIN AUTO-GENERATED CODE\n" + INDENT + INDENT + "if key ~= nil then\n"
    input_code += INDENT + INDENT + INDENT + "if key.key == 'ESC' then\n"
    input_code += INDENT + INDENT + INDENT + INDENT + "cene.quit = true\n"
    input_code += INDENT + INDENT + INDENT + "end\n"
    input_code += INDENT + INDENT + "end\n"
    input_code += INDENT + INDENT + "-- END AUTO-GENERATED CODE\n\n"
    return fill_section(content, "%%INPUT_CODE%%", input_code)


def fill_cleanup_data(content, room_name):
    import hpms_fncall_templates
    import hpms_filters
    entities = hpms_filters.filter_entities(room_name)
    cleanup_code = INDENT + INDENT + "-- BEGIN AUTO-GENERATED CODE\n" + INDENT + INDENT + "hpms.clean_scene(scene)\n\n"

    cameras = hpms_filters.filter_cameras(room_name)
    for cam in cameras:
        cam_name = cam.name
        cleanup_code += INDENT + INDENT + fill_section(hpms_fncall_templates.DELETE_DEPTH_MASK, "%%CAM_NAME%%",
                                                       cam_name) + "\n"
        cleanup_code += INDENT + INDENT + fill_section(hpms_fncall_templates.DELETE_BACKGROUND, "%%CAM_NAME%%",
                                                       cam_name) + "\n"

    cleanup_code += "\n"

    for ent in entities:
        ent_name = ent.name
        cleanup_code += INDENT + INDENT + fill_section(hpms_fncall_templates.DELETE_ENTITY, "%%ENT_NAME%%",
                                                       ent_name) + "\n"

    cleanup_code += "\n"

    cleanup_code += INDENT + INDENT + fill_section(hpms_fncall_templates.DELETE_FLOOR, "%%ROOM_NAME%%",
                                                   room_name) + "\n"
    cleanup_code += INDENT + INDENT + "-- END AUTO-GENERATED CODE\n\n"
    return fill_section(content, "%%CLEANUP_CODE%%", cleanup_code)


def fill_object_position_rotation(location, pos, rot):
    location = fill_section(location, "%%PX%%", pos.x)
    location = fill_section(location, "%%PY%%", pos.z)
    location = fill_section(location, "%%PZ%%", -pos.y)
    location = fill_section(location, "%%RX%%", radians(90) - rot.x)
    location = fill_section(location, "%%RY%%", -rot.z)
    location = fill_section(location, "%%RZ%%", rot.y)
    return location


def fill_object_scale(location, scale):
    location = fill_section(location, "%%SX%%", scale.x)
    location = fill_section(location, "%%SY%%", scale.y)
    location = fill_section(location, "%%SZ%%", scale.z)
    return location


def fill_blender_data(path, room_name):
    script = path + "/" + room_name + ".lua"
    with open(script, 'r') as file:
        content = file.read()
    content = fill_section(content, "%%ROOM_NAME%%", room_name)
    content = fill_setup_data(content, room_name)
    content = fill_input_data(content)
    content = fill_update_data(content, room_name)
    content = fill_cleanup_data(content, room_name)
    with open(script, 'w') as file:
        file.write(content)


def update_room(path, room_name):
    sections = get_user_code(path, room_name)
    create_room(path, room_name, False)
    script = path + "/" + room_name + ".lua"
    with open(script, 'r') as file:
        content = file.read()

    content = fill_section(content, "%%SETUP_USER_CODE%%", sections[0])
    content = fill_section(content, "%%INPUT_USER_CODE%%", sections[1])
    content = fill_section(content, "%%UPDATE_USER_CODE%%", sections[2])
    content = fill_section(content, "%%CLEANUP_USER_CODE%%", sections[3])
    content = fill_section(content, "%%FUNCTIONS_USER_CODE%%", sections[4])
    with open(script, 'w') as file:
        file.write(content)


def remove_user_placeholders(path, room_name):
    script = path + "/" + room_name + ".lua"
    with open(script, 'r') as file:
        content = file.read()

    content = fill_section(content, "%%SETUP_USER_CODE%%", "")
    content = fill_section(content, "%%INPUT_USER_CODE%%", "")
    content = fill_section(content, "%%UPDATE_USER_CODE%%", "")
    content = fill_section(content, "%%CLEANUP_USER_CODE%%", "")
    content = fill_section(content, "%%FUNCTIONS_USER_CODE%%", "")
    with open(script, 'w') as file:
        file.write(content)


def create_room(path, room_name, clean_placeholders):
    import shutil
    template = hpms_utils.get_current_dir() + "/templates/template_room.txt"
    script = path + "/" + room_name + ".lua"
    shutil.copyfile(template, script)
    if clean_placeholders:
        remove_user_placeholders(path, room_name)


def create_or_update_room_script(path, room_name, room_list, update_all):
    script = path + "/" + room_name + ".lua"
    if os.path.exists(script):
        if update_all or room_name in room_list:
            hpms_utils.debug("Updating room " + room_name)
            update_room(path, room_name)
        else:
            hpms_utils.debug("Skipping room " + room_name)
            return
    else:
        hpms_utils.debug("Creating room " + room_name)
        create_room(path, room_name, True)

    fill_blender_data(path, room_name)
