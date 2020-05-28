#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    HPMS plugin for export base walkmap and sector groups calculation.
    Author: Ray1184
    Version: 1.0
"""

import bpy
from bpy.props import *
from bpy_extras.io_utils import ExportHelper


class HPMSWalkmapExporter(bpy.types.Operator, ExportHelper):
    bl_idname = "export.json"
    bl_label = "Export JSON"

    filename_ext = ".json"

    def invoke(self, context, event):
        return ExportHelper.invoke(self, context, event)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        print("Selected: " + context.active_object.name)

        if not self.properties.filepath:
            raise Exception("filename not set")

        filepath = self.filepath

        import io_mesh_json.export_json
        return io_mesh_json.export_json.save(self, context, **self.properties)

    def menu_func_export(self, context):
        default_path = bpy.data.filepath.replace(".blend", ".json")
        self.layout.operator(ExportJSON.bl_idname, text="JSON (.json)").filepath = default_path

        def register():
            bpy.utils.register_module(__name__)
            bpy.types.INFO_MT_file_export.append(menu_func_export)
            bpy.types.INFO_MT_file_import.append(menu_func_import)

        def unregister():
            bpy.utils.unregister_module(__name__)
            bpy.types.INFO_MT_file_export.remove(menu_func_export)
            bpy.types.INFO_MT_file_import.remove(menu_func_import)
