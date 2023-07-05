# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/1d_stairs_sketcher

import bmesh
import bpy
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class

bl_info = {
    "name": "Stairs Sketcher",
    "description": "Creates stairs line from selected loop",
    "author": "Nikita Akimov, Paul Kotelevets",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Tool panel > 1D > Stairs Sketcher",
    "doc_url": "https://github.com/Korchy/1d_stairs_sketcher",
    "tracker_url": "https://github.com/Korchy/1d_stairs_sketcher",
    "category": "All"
}


# MAIN CLASS

class StairsSketcher:
    pass

    @classmethod
    def create_stairs_line(cls, context):
        # Create stairs line from selected loop
        print('create stairs line')
        # # current mode
        # mode = context.active_object.mode
        # # switch to Edit mode
        # if context.active_object.mode == 'OBJECT':
        #     bpy.ops.object.mode_set(mode='EDIT')
        # # switch to edges mode
        # context.tool_settings.mesh_select_mode = (False, True, False)
        # # switch to Object mode
        # bpy.ops.object.mode_set(mode='OBJECT')
        # # deselect all data
        # cls._deselect_all(obj_data=context.object.data)
        # # select UV-Seam edges and set crease by them
        # bm = bmesh.new()
        # bm.from_mesh(context.object.data)
        # bm.edges.ensure_lookup_table()
        # # select seam edges
        # seam_edges = [e for e in bm.edges if e.seam]
        # for edge in seam_edges:
        #     edge.select = True
        # # set crease
        # crease_layer = bm.edges.layers.crease.verify()
        # for edge in bm.edges:
        #     if edge.select:
        #         edge[crease_layer] = 1.0
        #     else:
        #         edge[crease_layer] = 0.0
        # # save changed data to mesh
        # bm.to_mesh(context.object.data)
        # # return mode back
        # bpy.ops.object.mode_set(mode=mode)
    #
    # @staticmethod
    # def _deselect_all(obj_data):
    #     for polygon in obj_data.polygons:
    #         polygon.select = False
    #     for edge in obj_data.edges:
    #         edge.select = False
    #     for vertex in obj_data.vertices:
    #         vertex.select = False


# OPERATORS

class StairsSketcher_OT_create_line(Operator):
    bl_idname = 'stairs_sketcher.create_line'
    bl_label = 'Stairs Sketcher'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        StairsSketcher.create_stairs_line(
            context=context
        )
        return {'FINISHED'}


# PANELS

class StairsSketcher_PT_panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Stairs Sketcher"
    bl_category = '1D'

    def draw(self, context):
        layout = self.layout
        layout.operator(
            operator='stairs_sketcher.create_line',
            icon='IPO_CONSTANT'
        )


# REGISTER

def register():
    register_class(StairsSketcher_OT_create_line)
    register_class(StairsSketcher_PT_panel)


def unregister():
    unregister_class(StairsSketcher_PT_panel)
    unregister_class(StairsSketcher_OT_create_line)


if __name__ == "__main__":
    register()
