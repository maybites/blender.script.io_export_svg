#  ***** GPL LICENSE BLOCK *****
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
#  ***** GPL LICENSE BLOCK *****

bl_info = {
    "name": "Export SVG Format (.svg)",
    "author": "Martin Froehlich (maybites.ch) + Matthew Ready (craxic.com)",
    "version": (0, 0, 6),
    "blender": (2, 7, 0),
    "location": "File > Export > Inkscape (.svg)",
    "description": "The script exports Blender BezierCurves to SVG format.",
    "warning": "Quick and dirty hack, no success guaranteed. Doesn't like objectnames with special characters",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Import-Export/Inkscape_SVG_Exporter",
    "tracker_url": "",
    "category": "Import-Export"
}

# Ensure that we reload our dependencies if we ourselves are reloaded by Blender
if "bpy" in locals():
    import imp;
    if "exporter" in locals():
        imp.reload(exporter);
        
import bpy;
from .exporter import Exporter;

def menu_func(self, context):
    self.layout.operator(Exporter.bl_idname, text="Inkscape (.svg)");

def register():
    bpy.utils.register_module(__name__);
    bpy.types.INFO_MT_file_export.append(menu_func);
    
def unregister():
    bpy.utils.unregister_module(__name__);
    bpy.types.INFO_MT_file_export.remove(menu_func);

if __name__ == "__main__":
    register()
