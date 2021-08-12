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

import bpy
from bpy.types import Panel

class COLOR_SELECTOR_PT_selector_panel(Panel):
    bl_label = "Color Selector"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        def draw_UI():
            selected_objects = bpy.context.selected_objects
            if not selected_objects:
                return False
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

        COLOR_NUM = 8

        layout = self.layout
        row = layout.row(align=True)
        row.label(text="Color Selector1")

        box = layout.box()
        row = box.row(align=True)
        row.operator("color_selector.start", text="Start")
        row.operator("color_selector.end", text="End")

        if draw_UI():
            for i in range(COLOR_NUM):
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



def register():
    bpy.utils.register_class(COLOR_SELECTOR_PT_selector_panel)

def unregister():
    bpy.utils.unregister_class(COLOR_SELECTOR_PT_selector_panel)


if __name__ == '__main__':
    register()
