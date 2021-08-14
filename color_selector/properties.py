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
from bpy.types import PropertyGroup
from bpy.props import PointerProperty, BoolProperty


class ColorSelectorProps(PropertyGroup):
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


def register():
    bpy.utils.register_class(ColorSelectorProps)
    bpy.types.Scene.colorSelectorProps = PointerProperty(type=ColorSelectorProps)



def unregister():
    del bpy.types.Scene.colorSelectorProps
    bpy.utils.unregister_class(ColorSelectorProps)


if __name__ == '__main__':
    register()
