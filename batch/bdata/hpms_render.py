import os
import shutil
from math import radians

import bpy

TYPE_IMAGE = 0
TYPE_DEPTH = 1

# Cam settings
CAM_FOV = 60
Z_NEAR = 0.1
Z_FAR = 50

# Rendering settings
DEVICE = "GPU"
WIDTH = 320
HEIGHT = 200
FILTER_WIDTH = 0.01
EXPOSURE = 1.5
PREVIEW_SAMPLES = 16
SAMPLES = 512
MAX_BOUNCES = 0
CLAMP_INDIRECT = 1
MAP_RESOLUTION = 1024


def update_screens(img_path, depth_path, room_name):
    shutil.rmtree(img_path + "/" + room_name, ignore_errors=True)
    shutil.rmtree(depth_path + "/" + room_name, ignore_errors=True)
    create_screens(img_path, depth_path, room_name)


def config_cam(cam):
    cam.lens_unit = "FOV"
    cam.sensor_fit = "VERTICAL"
    cam.angle = radians(CAM_FOV)
    cam.clip_start = Z_NEAR
    cam.clip_end = Z_FAR


def clear_compositing_tree(tree):
    for node in tree.nodes:
        tree.nodes.remove(node)
    for link in tree.links:
        tree.links.remove(link)


def setup_image_workflow():
    bpy.context.scene.view_settings.view_transform = "Standard"
    bpy.context.scene.sequencer_colorspace_settings.name = "sRGB"
    tree = bpy.context.scene.node_tree
    clear_compositing_tree(tree)
    rend_node = tree.nodes.new("CompositorNodeRLayers")
    comp_node = tree.nodes.new("CompositorNodeComposite")
    tree.links.new(rend_node.outputs["Image"], comp_node.inputs["Image"])


def setup_depth_workflow():
    bpy.context.scene.view_settings.view_transform = "Raw"
    bpy.context.scene.sequencer_colorspace_settings.name = "Raw"
    tree = bpy.context.scene.node_tree
    clear_compositing_tree(tree)
    rend_node = tree.nodes.new("CompositorNodeRLayers")
    comp_node = tree.nodes.new("CompositorNodeComposite")
    sub_node = tree.nodes.new("CompositorNodeMath")
    sub_node.operation = "SUBTRACT"
    sub_node.inputs[1].default_value = Z_NEAR
    div_node = tree.nodes.new("CompositorNodeMath")
    div_node.operation = "DIVIDE"
    div_node.inputs[1].default_value = Z_FAR - Z_NEAR
    tree.links.new(rend_node.outputs["Depth"], sub_node.inputs[0])
    tree.links.new(sub_node.outputs["Value"], div_node.inputs[0])
    tree.links.new(div_node.outputs["Value"], comp_node.inputs["Image"])


def render_image(path, cam_name):
    bpy.context.scene.render.filepath = path + "/" + cam_name + ".png"

    img_type = "view"
    if "/masks/" in path:
        img_type = "depth mask"

    import hpms_utils
    hpms_utils.debug("Rendering " + img_type + " " + cam_name)

    from os import open, close, dup, O_WRONLY

    old = dup(1)
    close(1)
    open(hpms_utils.get_current_dir() + "/../syslogs/blender_render.log", O_WRONLY)
    bpy.ops.render.render(write_still=True)
    close(1)
    dup(old)
    close(old)


def configure_renderer(preview):
    bpy.context.scene.use_nodes = True

    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.render.resolution_x = WIDTH
    bpy.context.scene.render.resolution_y = HEIGHT
    bpy.context.scene.render.resolution_percentage = 100

    bpy.context.scene.cycles.device = DEVICE
    bpy.context.scene.cycles.filter_type = "GAUSSIAN"
    bpy.context.scene.cycles.filter_width = FILTER_WIDTH
    bpy.context.scene.cycles.aa_samples = 1
    bpy.context.scene.cycles.film_exposure = EXPOSURE
    if preview:
        bpy.context.scene.cycles.samples = PREVIEW_SAMPLES
    else:
        bpy.context.scene.cycles.samples = SAMPLES

    bpy.context.scene.cycles.sample_clamp_indirect = CLAMP_INDIRECT
    bpy.context.scene.cycles.glossy_bounces = MAX_BOUNCES
    bpy.context.scene.world.cycles.sample_as_light = True
    bpy.context.scene.world.cycles.sample_map_resolution = MAP_RESOLUTION


def create_screen(path, cam):
    bpy.context.scene.camera = cam
    render_image(path, cam.name)


def create_screens(img_path, depth_path, room_name):
    os.makedirs(img_path + "/" + room_name)
    os.makedirs(depth_path + "/" + room_name)
    import hpms_filters
    room_cams = hpms_filters.filter_cameras(room_name)
    setup_image_workflow()
    for cam in room_cams:
        create_screen(img_path + "/" + room_name, cam)
    setup_depth_workflow()
    for cam in room_cams:
        create_screen(depth_path + "/" + room_name, cam)


def create_or_update_screens(img_path, depth_path, room_name, room_list, update_all):
    screen = img_path + "/" + room_name
    depth = depth_path + "/" + room_name
    if os.path.exists(screen) or os.path.exists(depth):
        if update_all or room_name in room_list:
            update_screens(img_path, depth_path, room_name)

    else:
        create_screens(img_path, depth_path, room_name)
