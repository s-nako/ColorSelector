# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import bpy
from bpy.types import Operator
from . import utils

def add_materials():
    COLOR_NUM = 8
    obj = bpy.context.active_object
    if not obj:
        return
    bpy.ops.object.mode_set(mode='OBJECT')
    if obj.type != "MESH":
        return

    for i in range(COLOR_NUM):
        if "ColorSelectorMaterial" + str(i) not in bpy.data.materials:
            material = bpy.data.materials.new("ColorSelectorMaterial" + str(i))
            material.diffuse_color = list(utils.hsv2rgb(i / COLOR_NUM, 0.9, 1.0)) + [1.0]
    if "ColorSelectorMaterial_default" not in bpy.data.materials:
        bpy.data.materials.new("ColorSelectorMaterial_default")

    if hasattr(obj.data, 'materials'):
        mat_name = "ColorSelectorMaterial_default"
        if mat_name not in obj.data.materials:
            obj.data.materials.append(bpy.data.materials[mat_name])
        for i in range(COLOR_NUM):
            mat_name = "ColorSelectorMaterial" + str(i)
            if mat_name not in obj.data.materials:
                obj.data.materials.append(bpy.data.materials[mat_name])
        bpy.ops.object.material_slot_assign()
    bpy.ops.object.mode_set(mode='EDIT')


def remove_materials():
    obj = bpy.context.active_object
    if obj and hasattr(obj.data, 'materials'):
        i = 0
        for material in obj.data.materials:
            if material and material.name.startswith("ColorSelectorMaterial"):
                obj.data.materials.pop(index=i)
            else:
                i += 1


def delete_all_materials():
    objs = bpy.data.objects
    for obj in objs:
        if hasattr(obj.data, 'materials'):
            i = 0
            for material in obj.data.materials:
                if material and material.name.startswith("ColorSelectorMaterial"):
                    obj.data.materials.pop(index=i)
                else:
                    i += 1
    for material in bpy.data.materials:
        if material.name.startswith("ColorSelectorMaterial"):
            bpy.data.materials.remove(material)


class COLOR_SELECTOR_OT_start(Operator):
    bl_idname = 'color_selector.start'
    bl_label = "Start"
    bl_options = {'REGISTER'}

    def execute(self, context):
        add_materials()
        return {'FINISHED'}


class COLOR_SELECTOR_OT_end(Operator):
    bl_idname = 'color_selector.end'
    bl_label = "End"
    bl_options = {'REGISTER'}

    def execute(self, context):
        remove_materials()
        return {'FINISHED'}


class COLOR_SELECTOR_OT_select(Operator):
    bl_idname = 'color_selector.select'
    bl_label = "Select"
    bl_options = {'REGISTER'}

    index: bpy.props.IntProperty(name="index")

    def execute(self, context):
        material_name = "ColorSelectorMaterial{}".format(self.index)
        obj = bpy.context.active_object
        bpy.ops.mesh.select_mode(type="FACE")
        if material_name in obj.data.materials:
            obj.active_material_index = obj.data.materials.find(material_name)
            bpy.ops.object.material_slot_select()
        return {'FINISHED'}


class COLOR_SELECTOR_OT_assign(Operator):
    bl_idname = 'color_selector.assign'
    bl_label = "Assign"
    bl_options = {'REGISTER'}

    index: bpy.props.IntProperty(name="index")

    def execute(self, context):
        material_name = "ColorSelectorMaterial{}".format(self.index)
        obj = bpy.context.active_object
        if not obj.data.materials:
            obj.data.materials.append(bpy.data.materials["ColorSelectorMaterial_default"])
        if material_name not in obj.data.materials:
            obj.data.materials.append(bpy.data.materials[material_name])
        obj.active_material_index = obj.data.materials.find(material_name)
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.object.material_slot_assign()
        return {'FINISHED'}


class COLOR_SELECTOR_OT_release(Operator):  # release means set default
    bl_idname = 'color_selector.release'
    bl_label = "Release"
    bl_options = {'REGISTER'}

    index: bpy.props.IntProperty(name="index")

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        for polygon in bpy.context.active_object.data.polygons:
            polygon.select = False
        for edge in bpy.context.active_object.data.edges:
            edge.select = False
        for vertex in bpy.context.active_object.data.vertices:
            vertex.select = False
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.color_selector.select(index=self.index)
        objs = [bpy.context.active_object]
        mat_name = "ColorSelectorMaterial_default"
        for obj in objs:
            if hasattr(obj.data, 'materials'):
                obj.active_material_index = obj.data.materials.find(mat_name)
                bpy.ops.object.material_slot_assign()
        return {'FINISHED'}


def deselect_all():
    bpy.ops.object.mode_set(mode='OBJECT')
    for polygon in bpy.context.active_object.data.polygons:
        polygon.select = False
    for edge in bpy.context.active_object.data.edges:
        edge.select = False
    for vertex in bpy.context.active_object.data.vertices:
        vertex.select = False
    bpy.ops.object.mode_set(mode='EDIT')


class COLOR_SELECTOR_OT_hide(Operator):
    bl_idname = 'color_selector.hide'
    bl_label = "Hide"
    bl_options = {'REGISTER'}

    index: bpy.props.IntProperty(name="index")

    def execute(self, context):
        setattr(context.scene.colorSelectorProps, "show_hide_ID_{}".format(self.index), False)
        deselect_all()
        # bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.color_selector.select(index=self.index)
        bpy.ops.mesh.hide(unselected=False)
        # bpy.context.region.tag_redraw()
        return {'FINISHED'}


class COLOR_SELECTOR_OT_show(Operator):
    bl_idname = 'color_selector.show'
    bl_label = "Show"
    bl_options = {'REGISTER'}

    index: bpy.props.IntProperty(name="index")

    def execute(self, context):
        setattr(context.scene.colorSelectorProps, "show_hide_ID_{}".format(self.index), True)
        bpy.ops.mesh.reveal()
        deselect_all()
        # bpy.ops.mesh.select_mode(type="FACE")
        COLOR_NUM = 8
        for i in range(COLOR_NUM):
            show = getattr(context.scene.colorSelectorProps, "show_hide_ID_{}".format(i))
            if not show:
                bpy.ops.color_selector.select(index=i)
        bpy.ops.mesh.hide(unselected=False)
        # bpy.context.region.tag_redraw()
        return {'FINISHED'}


classes = [
    COLOR_SELECTOR_OT_start,
    COLOR_SELECTOR_OT_end,
    COLOR_SELECTOR_OT_select,
    COLOR_SELECTOR_OT_assign,
    COLOR_SELECTOR_OT_release,
    COLOR_SELECTOR_OT_hide,
    COLOR_SELECTOR_OT_show
]


def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == '__main__':
    register()
