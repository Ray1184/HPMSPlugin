import os
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


def fill_user_section(content, from_string, to_string):
    if to_string is None or to_string == "":
        to_string = ""
    else:
        to_string = to_string.rstrip()
    return content.replace(from_string, to_string)


def fill_blender_data(path, room_name):
    script = path + "/" + room_name + ".lua"
    with open(script, 'r') as file:
        content = file.read()
    content = fill_user_section(content, "%%ROOM_NAME%%", room_name)
    with open(script, 'w') as file:
        file.write(content)


def update_room(path, room_name):
    sections = get_user_code(path, room_name)
    create_room(path, room_name, False)
    script = path + "/" + room_name + ".lua"
    with open(script, 'r') as file:
        content = file.read()

    content = fill_user_section(content, "%%SETUP_USER_CODE%%", sections[0])
    content = fill_user_section(content, "%%INPUT_USER_CODE%%", sections[1])
    content = fill_user_section(content, "%%UPDATE_USER_CODE%%", sections[2])
    content = fill_user_section(content, "%%CLEANUP_USER_CODE%%", sections[3])
    content = fill_user_section(content, "%%FUNCTIONS_USER_CODE%%", sections[4])
    with open(script, 'w') as file:
        file.write(content)


def remove_user_placeholders(path, room_name):
    script = path + "/" + room_name + ".lua"
    with open(script, 'r') as file:
        content = file.read()

    content = fill_user_section(content, "%%SETUP_USER_CODE%%", "")
    content = fill_user_section(content, "%%INPUT_USER_CODE%%", "")
    content = fill_user_section(content, "%%UPDATE_USER_CODE%%", "")
    content = fill_user_section(content, "%%CLEANUP_USER_CODE%%", "")
    content = fill_user_section(content, "%%FUNCTIONS_USER_CODE%%", "")
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
