blender.script.io_export_svg
===============

exportscript for blender 2.68 to get BezierCurves to SVG. for more info please go [there](http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Import-Export/Inkscape_SVG_Exporter)

Getting
---

Best way is to:

git clone https://github.com/maybites/blender.script.io_export_svg

and symlinking it to your addons-folder.

That way, you can git pull later on and it will automatically refresh to the latest (theoretically-)good version.


Lasercutting
---

If you want to export the SVG for precise lasercutting and since the laser is not a precis point (in the folling example 0.2mm in diameter, but its depending on the machine), you have to ajust the vector with an outset (or inset). After exporting the SVG you can do that in almost any vector-drawing program, here the instructions for Inkscape:

1. Open the exported SVG-file
2. Press Shift+Ctrl+D
3. Change Standard units to mm
4. Change Userdefined units to mm and close the documents properties
5. Select the vector to change
6. Change the line thickness to 0.1mm
7. Zoom close to the line (to the upper left corner of the object, thats where the little handle of the next steps will appear) and set a help line on to the outer-perimeter of the vector. Set it to the inner-perimeter if you want to create an inset.
8. Switch to Path-modify-tool
9. Select Menu->Path->Dynamic Outset¨
10. Grab the little handle and set the inner-perimeter (or outer-perimeter for an inset) of the vector onto the previously set help-line
11. If your lasercutter needs a special linethickness to recognise the cutline, set the linethickness accordingly.
12. Done. 

Your vector is now exacly a 0.1mm perimeter of the previous form, and the laser will cut right at the edge of the shape you defined in blender. 

