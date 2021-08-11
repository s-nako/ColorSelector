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
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "Color Selector Test",
    "author": "Nako",
    "description": "select or show/hide meshes by color on the UI",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "doc_url": "https://github.com/s-nako/color_selector",
    "tracker_url": "https://github.com/s-nako/color_selector/issues",
    "category": "3D View",
}

import bpy
from bpy.types import (Menu, Operator, Panel, AddonPreferences, PropertyGroup)
from bpy.props import (FloatVectorProperty, PointerProperty, BoolProperty)


def hsv2rgb(h, s, v):
    c = v * s
    h2 = h * 360 / 60
    x = c * (1.0 - abs(h2 % 2 - 1))
    r = v - c
    g = v - c
    b = v - c
    h2_int = h * 360 // 60
    if h2_int == 0:
        return r + c, g + x, b
    elif h2_int == 1:
        return r + x, g + c, b
    elif h2_int == 2:
        return r, g + c, b + x
    elif h2_int == 3:
        return r, g + x, b + c
    elif h2_int == 4:
        return r + x, g, b + c
    elif h2_int == 5:
        return r + c, g, b + x
    elif h2_int == 6:
        return r + c, g + x, b


def add_materials():
    count = 8
    for i in range(count):
        if "ColorSelectorMaterial" + str(i) not in bpy.data.materials:
            material = bpy.data.materials.new("ColorSelectorMaterial" + str(i))
            material.diffuse_color = list(hsv2rgb(i / count, 0.9, 1.0)) + [1.0]
    if "ColorSelectorMaterial_default" not in bpy.data.materials:
        bpy.data.materials.new("ColorSelectorMaterial_default")
    if not bpy.context.active_object:
        return
    bpy.ops.object.mode_set(mode='OBJECT')
    obj = bpy.context.active_object
    if hasattr(obj.data, 'materials'):
        mat_name = "ColorSelectorMaterial_default"
        if mat_name not in obj.data.materials:
            obj.data.materials.append(bpy.data.materials[mat_name])
        for i in range(count):
            mat_name = "ColorSelectorMaterial" + str(i)
            if mat_name not in obj.data.materials:
                obj.data.materials.append(bpy.data.materials[mat_name])
        bpy.ops.object.material_slot_assign()
    bpy.ops.object.mode_set(mode='EDIT')


def remove_materials():
    obj = bpy.context.active_object
    if hasattr(obj.data, 'materials'):
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


class COLOR_SELECTOR_OT_start(bpy.types.Operator):
    bl_idname = 'color_selector.start'
    bl_label = "Start"
    bl_options = {'REGISTER'}

    def execute(self, context):
        add_materials()
        return {'FINISHED'}


class COLOR_SELECTOR_OT_end(bpy.types.Operator):
    bl_idname = 'color_selector.end'
    bl_label = "End"
    bl_options = {'REGISTER'}

    def execute(self, context):
        remove_materials()
        return {'FINISHED'}


class COLOR_SELECTOR_OT_select(bpy.types.Operator):
    bl_idname = 'color_selector.select'
    bl_label = "Select"
    bl_options = {'REGISTER'}

    index: bpy.props.IntProperty(name="index")

    def execute(self, context):  # eventloop should be here
        material_name = "ColorSelectorMaterial{}".format(self.index)
        obj = bpy.context.active_object
        bpy.ops.mesh.select_mode(type="FACE")
        if material_name in obj.data.materials:
            obj.active_material_index = obj.data.materials.find(material_name)
            bpy.ops.object.material_slot_select()
        return {'FINISHED'}


class COLOR_SELECTOR_OT_assign(bpy.types.Operator):
    bl_idname = 'color_selector.assign'
    bl_label = "Assign"
    bl_options = {'REGISTER'}

    index: bpy.props.IntProperty(name="index")

    def execute(self, context):  # eventloop should be here
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


class COLOR_SELECTOR_OT_release(bpy.types.Operator):  # release means set default
    bl_idname = 'color_selector.release'
    bl_label = "Release"
    bl_options = {'REGISTER'}

    index: bpy.props.IntProperty(name="index")

    def execute(self, context):  # eventloop should be here
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


class COLOR_SELECTOR_OT_hide(bpy.types.Operator):
    bl_idname = 'color_selector.hide'
    bl_label = "Hide"
    bl_options = {'REGISTER'}

    index: bpy.props.IntProperty(name="index")

    def execute(self, context):  # eventloop should be here
        setattr(context.scene.colorSelectorProps, "show_hide_ID_{}".format(self.index), False)
        deselect_all()
        # bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.color_selector.select(index=self.index)
        bpy.ops.mesh.hide(unselected=False)
        # bpy.context.region.tag_redraw()
        return {'FINISHED'}


class COLOR_SELECTOR_OT_show(bpy.types.Operator):
    bl_idname = 'color_selector.show'
    bl_label = "Show"
    bl_options = {'REGISTER'}

    index: bpy.props.IntProperty(name="index")

    def execute(self, context):  # eventloop should be here
        setattr(context.scene.colorSelectorProps, "show_hide_ID_{}".format(self.index), True)
        bpy.ops.mesh.reveal()
        deselect_all()
        # bpy.ops.mesh.select_mode(type="FACE")
        count = 8
        for i in range(count):
            show = getattr(context.scene.colorSelectorProps, "show_hide_ID_{}".format(i))
            if not show:
                bpy.ops.color_selector.select(index=i)
        bpy.ops.mesh.hide(unselected=False)
        # bpy.context.region.tag_redraw()
        return {'FINISHED'}


class COLOR_SELECTOR_PT_selector_panel(bpy.types.Panel):
    bl_label = "Color Selector"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        # print("refraw UI panel")
        def draw_UI():
            selected_objects = bpy.context.selected_objects
            if selected_objects:
                for obj in selected_objects:
                    if obj.type == "MESH":
                        break
                else:
                    return False
            active_object = bpy.context.active_object
            if not active_object or active_object.type != "MESH":
                return False
            if hasattr(active_object.data, 'materials'):
                for material in active_object.data.materials:
                    if material and material.name.startswith("ColorSelectorMaterial"):
                        return True
            return False

        MAX_COLOR_NUM = 8

        layout = self.layout
        row = layout.row(align=True)
        row.label(text="Color Selector1")

        box = layout.box()
        row = box.row(align=True)
        row.operator("color_selector.start", text="Start")
        row.operator("color_selector.end", text="End")

        if draw_UI():
            for i in range(MAX_COLOR_NUM):
                row = box.row(align=True)
                row.prop(context.scene.colorSelectorProps, "color_ID_color_{}".format(i), text="")
                if getattr(context.scene.colorSelectorProps, "show_hide_ID_{}".format(i)):
                    hide_op = row.operator("color_selector.hide", text="Show")
                    hide_op.index = i
                else:
                    show_op = row.operator("color_selector.show", text="Hide", depress=True)
                    show_op.index = i

                select_op = row.operator("color_selector.select", text="Select")
                select_op.index = i
                assign_op = row.operator("color_selector.assign", text="Assign")
                assign_op.index = i
                release_op = row.operator("color_selector.release", text="×")
                release_op.index = i


class ColorSelectorProps(PropertyGroup):
    def get_color(i):
        return FloatVectorProperty(
            name="Color",
            description="Set Color for the Palette",
            subtype="COLOR",
            default=hsv2rgb(i / 8, 0.9, 1.0),
            size=3,
            max=1.0, min=0.0
        )

    color_ID_color_0: get_color(0)
    color_ID_color_1: get_color(1)
    color_ID_color_2: get_color(2)
    color_ID_color_3: get_color(3)
    color_ID_color_4: get_color(4)
    color_ID_color_5: get_color(5)
    color_ID_color_6: get_color(6)
    color_ID_color_7: get_color(7)

    def show_hide_param():
        return BoolProperty(
            description="Show/Hide elements",
            default=True
        )

    show_hide_ID_0: show_hide_param()
    show_hide_ID_1: show_hide_param()
    show_hide_ID_2: show_hide_param()
    show_hide_ID_3: show_hide_param()
    show_hide_ID_4: show_hide_param()
    show_hide_ID_5: show_hide_param()
    show_hide_ID_6: show_hide_param()
    show_hide_ID_7: show_hide_param()


classs = [
    ColorSelectorProps,
    COLOR_SELECTOR_OT_start,
    COLOR_SELECTOR_OT_end,
    COLOR_SELECTOR_OT_select,
    COLOR_SELECTOR_OT_assign,
    COLOR_SELECTOR_OT_release,
    COLOR_SELECTOR_OT_hide,
    COLOR_SELECTOR_OT_show,
    COLOR_SELECTOR_PT_selector_panel
]


def register():
    for c in classs:
        bpy.utils.register_class(c)
    bpy.types.Scene.colorSelectorProps = PointerProperty(type=ColorSelectorProps)


def unregister():
    del bpy.types.Scene.colorSelectorProps
    for c in classs:
        bpy.utils.unregister_class(c)
    delete_all_materials()


if __name__ == '__main__':
    register()
