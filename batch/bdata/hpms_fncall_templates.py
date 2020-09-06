MAKE_ENTITY = "e_%%ENT_NAME%% = hpms.make_entity(\"data/models/%%ENT_NAME%%.hmdat\")"
MAKE_BACKGROUND = "b_%%CAM_NAME%% = hpms.make_background(\"data/screens/%%CAM_NAME%%.png\")"
MAKE_DEPTH_MASK = "dm_%%CAM_NAME%% = hpms.make_depth_mask(\"data/masks/%%CAM_NAME%%.png\")"
MAKE_FLOOR = "f_%%ROOM_NAME%% = hpms.make_floor(\"data/maps/%%ROOM_NAME%%.hfdat\")"
MAKE_ENTITY_COLLISOR = "cls_%%ENT_NAME%% = hpms.make_collisor(e_%%ENT_NAME%%, f_%%ROOM_NAME%%)"

ADD_ENTITY = "hpms.add_entity_to_scene(e_%%ENT_NAME%%, scene)"
ADD_BACKGROUND = "hpms.add_picture_to_scene(b_%%CAM_NAME%%, scene)"
ADD_DEPTH_MASK = "hpms.add_picture_to_scene(dm_%%CAM_NAME%%, scene)"

DELETE_ENTITY = "hpms.delete_entity(e_%%ENT_NAME%%)"
DELETE_BACKGROUND = "hpms.delete_background(b_%%CAM_NAME%%)"
DELETE_DEPTH_MASK = "hpms.delete_depth_mask(dm_%%CAM_NAME%%)"
DELETE_FLOOR = "hpms.delete_floor(f_%%ROOM_NAME%%)"
DELETE_ENTITY_COLLISOR = "hpms.delete_collisor(cls_%%ENT_NAME%%)"

POS_ROT_SCALE = "common.pos_rot_scale(e_%%ENT_NAME%%, %%PX%%, %%PY%%, %%PZ%%, %%RX%%, %%RY%%, %%RZ%%, %%SX%%, " \
                "%%SY%%, %%SZ%%)"

ON_SECTOR_CHANGE_VIEW = "common.on_sector_change_view(camera, scene, f_%%ROOM_NAME%%, e_%%ENT_NAME%%, " \
                        "\"%%SECTOR_NAME%%\", %%PX%%, %%PY%%, %%PZ%%, %%RX%%, %%RY%%, %%RZ%%, b_%%CAM_NAME%%, " \
                        "dm_%%CAM_NAME%%) "

ON_ACTION_COLLECT = "common.on_action_collect(e_%%PL_ENT_NAME%%, e_%%PICK_ENT_NAME%%, %%TRHESHOLD%%)"
ON_ACTION_PUSH = "common.on_action_push(e_%%PL_ENT_NAME%%, e_%%PUSH_ENT_NAME%%, %%TRHESHOLD%%, %%DIRECTION%%)"
