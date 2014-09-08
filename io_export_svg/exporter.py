# --------------------------------------------------------------------------	
# Copyright (C) 2013: Martin Froehlich , maybites.ch
#
# based on code from the defunct export script by jm soler, jmsoler_at_free.fr
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# --------------------------------------------------------------------------

import bpy;
import struct;
from array import array;
from bpy_extras.io_utils import ExportHelper;
	   
class Exporter(bpy.types.Operator, ExportHelper):
	bl_idname       = "export_svg_format.svg";
	bl_label        = "Inkscape SVG Exporter";
	bl_options      = {'PRESET'};
	
	filename_ext    = ".svg";
				
	def execute(self, context):
		# Ensure Blender is currently in OBJECT mode to allow data access. 
		bpy.ops.object.mode_set(mode='OBJECT');
	
		# Set the default return state to FINISHED
		result = {'FINISHED'};
		
		# Check that the currently selected object contains mesh data for exporting
		curve = bpy.context.selected_objects[0];
		if not curve or curve.type != 'CURVE':
			raise NameError("Cannot export: object %s is not a curve" % curve);

		print(len(curve.data.splines));
		print(len(curve.data.splines[0].bezier_points));

		BoundingBox = curve.bound_box;
		B1=1000*((BoundingBox[3][0]-BoundingBox[0][0])**2.0 + (BoundingBox[3][1]-BoundingBox[0][1])**2.0 + (BoundingBox[3][2]-BoundingBox[0][2])**2.0)**0.5;
		B2=1000*((BoundingBox[7][0]-BoundingBox[3][0])**2.0 + (BoundingBox[7][1]-BoundingBox[3][1])**2.0 + (BoundingBox[7][2]-BoundingBox[3][2])**2.0)**0.5;

		xml_header="""<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">

<svg width="%smm" height="%smm"  viewBox="0 0 %s %s" xmlns="http://www.w3.org/2000/svg">
<title>Bezier Curve : %s</title>
	<desc>This is an exported Bezier xml_path from Blender, using the ExportScript by maybites.ch</desc>"""%(B2,B1,B2,B1,curve.name);
		xml_end="""</svg>""";

		shift=(BoundingBox[0][0]-curve.location[0])*1000, (curve.location[1]-BoundingBox[0][1])*1000;
		scaleX,scaleY,scaleZ=1000,1000,1000; #curve.dimensions * 500;
		scaleY*=-1.0;

		# Open the file for writing
		file = open(self.filepath, 'bw');
		file.write(bytes(xml_header, 'UTF-8'))
		
		splines = curve.data.splines;
		for spline in splines:
			
			if spline.type == 'BEZIER':
				n = 0;
				xml_path="""
		<g transform>
			<path style="fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
				d="svg_path"/></g>\n"""
				points = spline.bezier_points;
				for point in points:
					print(point.co);
					if n==0:
						svg_origin = [point.handle_left, point.co, point.handle_right];
						svg_path="M %s,%s\n"%(svg_origin[1][0]*scaleX,svg_origin[1][1]*scaleY+B1);
						previous_curve_point=svg_origin[2][0],svg_origin[2][1];
						n+=1;
					else:
						curve_point= [point.handle_left, point.co, point.handle_right];
						svg_path+="C %s,%s %s,%s %s,%s \n"%(previous_curve_point[0]*scaleX,
							previous_curve_point[1]*scaleY+B1,
							curve_point[0][0]*scaleX,
							curve_point[0][1]*scaleY+B1,
							curve_point[1][0]*scaleX,
							curve_point[1][1]*scaleY+B1);
						previous_curve_point=curve_point[2][0],curve_point[2][1];

				if spline.use_cyclic_u == 1:
					svg_path+="C %s,%s %s,%s %s,%s \n"%(previous_curve_point[0]*scaleX,
						previous_curve_point[1]*scaleY+B1,
						svg_origin[0][0]*scaleX,
						svg_origin[0][1]*scaleY+B1,
						svg_origin[1][0]*scaleX,
						svg_origin[1][1]*scaleY+B1);
					svg_path+="Z";
					
				xml_path=xml_path.replace('transform',"transform=\"translate(%s %s)\""%(-shift[0],-shift[1]))#shift[0],shift[1]));
				xml_path=xml_path.replace('svg_path',svg_path);
				file.write(bytes(xml_path, 'UTF-8'));

		file.write(bytes(xml_end, 'UTF-8'))
	   
		file.close();

		return result;
