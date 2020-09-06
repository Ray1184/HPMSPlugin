import bpy


def filter_entities(room_name):
    entities = [ent for ent in bpy.data.objects if room_name == ent.hpms_current_room and ent.name.startswith("EY_")]
    return entities


def filter_cameras(room_name):
    all_cams = [obj for obj in bpy.data.objects if obj.type == 'CAMERA']
    filtered_cams = []

    for cam in all_cams:
        for obj in bpy.data.objects:
            if obj.hpms_current_room == room_name and obj.hpms_current_cam == cam.name:
                filtered_cams.append(cam)

    return filtered_cams


def filter_sectors(room_name):
    sectors = [sec for sec in bpy.data.objects if room_name == sec.hpms_current_room and sec.name.startswith("SG_")]
    return sectors


def filter_player(room_name):
    entities = filter_entities(room_name)
    for ent in entities:
        if ent.hpms_entity_obj_prop.player == True:
            return ent
    raise Exception("One player must be defined for each room")
