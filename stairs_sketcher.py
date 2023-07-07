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
    def create_stairs_line(cls, context, op):
        # Create stairs line from selected loop
        src_obj = context.active_object
        # switch to Object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        # create new empty mesh
        stairs_mesh = context.blend_data.meshes.new('stairs')
        stairs_obj = context.blend_data.objects.new('stairs', stairs_mesh)
        stairs_obj.location = src_obj.location
        context.scene.objects.link(stairs_obj)
        # get data loop from source mesh
        bm = bmesh.new()
        bm.from_mesh(context.object.data)
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        # remove not-selected vertices
        [bm.verts.remove(vert) for vert in bm.verts if not vert.select]
        # source vertices
        src_vertices = [vert for vert in bm.verts]
        if src_vertices:
            top_vert = max([vert for vert in src_vertices], key=lambda vert: vert.co.z)
            first_vert = next((vert for vert in src_vertices
                               if len(vert.link_edges) == 1 and vert != top_vert), None)
            selection_loop_sorted = cls.vertices_loop_sorted(
                bmesh_vertices_list=src_vertices,
                bmesh_first_vertex=first_vert
            )
            stairs_height = top_vert.co.z - first_vert.co.z
            stair_height = stairs_height / len(src_vertices)
            # output stair_height to INFO
            op.report(
                type={'INFO'},
                message='stair height: ' + str(round(stair_height, 4))
            )
            # create stairs by sorted vertices
            prev_stair_vert = None
            for _i, vertex in enumerate(selection_loop_sorted):
                co_l = vertex.co.copy()     # lower stair point
                co_l.z = first_vert.co.z + stair_height * _i
                vert_l = bm.verts.new(co_l)
                co_h = vertex.co.copy()     # higher stair point
                co_h.z = first_vert.co.z + stair_height * (_i + 1)
                vert_h = bm.verts.new(co_h)
                bm.edges.new((vert_l, vert_h))
                if prev_stair_vert:
                    bm.edges.new((prev_stair_vert, vert_l))
                prev_stair_vert = vert_h
            # remove src vertices
            [bm.verts.remove(vert) for vert in src_vertices]
            # select all
            [vert.select_set(True) for vert in bm.verts if not vert.select]
        # save changed data to stairs mesh
        bm.to_mesh(stairs_mesh)
        bm.free()
        context.scene.objects.active = stairs_obj
        src_obj.select = False
        stairs_obj.select = True

    @staticmethod
    def vertices_loop_sorted(bmesh_vertices_list, bmesh_first_vertex):
        # return list with vertices sorted by following each other in the loop
        vertices_sorted = []
        if bmesh_vertices_list and bmesh_first_vertex:
            vertex = bmesh_first_vertex
            _l = len(bmesh_vertices_list)
            i = 0
            while vertex is not None:
                vertices_sorted.append(vertex)
                edge = next((_edge for _edge in vertex.link_edges
                             if _edge.other_vert(vertex) not in vertices_sorted), None)
                vertex = edge.other_vert(vertex) if edge else None
                # alarm break
                i += 1
                if i > _l:
                    print('_points_sorted() err exit')
                    break
        # return sorted sequence
        return vertices_sorted


# OPERATORS

class StairsSketcher_OT_create_line(Operator):
    bl_idname = 'stairs_sketcher.create_line'
    bl_label = 'Stairs Sketcher'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        StairsSketcher.create_stairs_line(
            context=context,
            op=self
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
