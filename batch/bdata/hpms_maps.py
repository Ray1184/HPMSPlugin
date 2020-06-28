import os
import shutil

import bpy


def update_map(path, room_name, sectors):
    shutil.rmtree(path + "/" + room_name + ".hfdat.raw", ignore_errors=True)
    create_map(path, room_name, sectors)


def create_map(path, room_name, sectors):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    [sector.select_set(True) for sector in sectors]
   
    bpy.ops.export_scene.obj(filepath=path + "/" + room_name + ".hfdat.raw", check_existing=False, axis_forward='-Z',
                             axis_up='Y',
                             filter_glob="*.obj;*.mtl", use_selection=True, use_animation=False,
                             use_mesh_modifiers=False, use_edges=False, use_smooth_groups=False,
                             use_smooth_groups_bitflags=False, use_normals=False, use_uvs=False, use_materials=False,
                             use_triangles=False, use_nurbs=False, use_vertex_groups=False, use_blen_objects=True,
                             group_by_object=False, group_by_material=False, keep_vertex_order=False, global_scale=1,
                             path_mode='AUTO')


def create_or_update_room_map(path, room_name, sectors, room_list, update_all):
    f_map = path + "/" + room_name + ".lua"
    if os.path.exists(f_map):
        if update_all or room_name in room_list:
            update_map(path, room_name, sectors)

    else:
        create_map(path, room_name, sectors)
