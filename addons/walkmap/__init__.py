#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    HPMS plugin for export base walkmap and sector groups calculation.
    Author: Ray1184
    Version: 1.0
"""

import bpy
from bpy_extras.io_utils import ExportHelper

bl_info = {
    "name": "HPMS Walkmap Exporter",
    "author": "Ray1184",
    "blender": (2, 82, 0),
    "version": (0, 0, 1),
    "location": "File > Import-Export",
    "description": "Export HPMS Walkmap data format",
    "category": "Import-Export",
    "wiki_url": "https://github.com/Ray1184/HPMSPlugin",
    "tracker_url": "https://github.com/Ray1184/HPMSPlugin",
}


class HPMSWalkmapExporter(bpy.types.Operator, ExportHelper):
    bl_idname = "export.hwmap"
    bl_label = "Export HPMS Walkmap"
    filename_ext = ".hwmap"

    def invoke(self, context, event):
        return ExportHelper.invoke(self, context, event)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        print("Selected: " + context.active_object.name)

        if not self.properties.filepath:
            raise Exception("filename not set")

        import walkmap.walkmap_exporter
        return walkmap.walkmap_exporter.save(self, context, **self.properties)


classes = (HPMSWalkmapExporter,)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


def menu_func_export(self, context):
    default_path = bpy.data.filepath.replace(".blend", ".hwmap")
    self.layout.operator(HPMSWalkmapExporter.bl_idname, text="HPMS Walkmap (.hwmap)").filepath = default_path


if __name__ == "__main__":
    register()
