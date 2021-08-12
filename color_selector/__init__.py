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
    "name": "Color Selector",
    "author": "Nako",
    "description": "select or show/hide meshes by color on the UI",
    "location": "View3D Tool tab",
    "version": (0, 8),
    "blender": (2, 80, 0),
    "doc_url": "https://github.com/s-nako/ColorSelector",
    "tracker_url": "https://github.com/s-nako/ColorSelector/issues",
    "category": "3D View",
}

import bpy
from . import properties
from . import operators
from . import ui_panel



def delete_all_materials():
    try:
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
    except:
        return


def register():
    print("register COLOR_SELECTOR")
    properties.register()
    operators.register()
    ui_panel.register()

def unregister():
    delete_all_materials()
    ui_panel.unregister()
    operators.unregister()
    properties.unregister()


if __name__ == '__main__':
    register()
