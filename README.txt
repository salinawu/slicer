Salina Wu & Kathleen Lu

------------------------------------------------------------------------------------------------------------------------------------

The main function is situated in gen_gcode.py.

Run the file gen_gcode.py from the command line:
% python gen_gcode.py filename.stl

There are default fill, perim thickness, and layer thickness values. You can change them either by
calling the function in the gen_gcode file or by changing the function default values.

This generates a gcode file with the equivalent name as filename.

------------------------------------------------------------------------------------------------------------------------------------

slicer.py contains code for parsing STL files, calculating triangle intersections, configuring the line segments
for each plane, calculating each plane's perimeter(s), etc.

contour_fill.py deals with generating line segments representing the fill of the insides of the polygons or perimeters;
these line segments are translated to gcode in gen_gcode.py.

shapes.py contains all of the class definitions for all of our shapes.

support.py looks through the object from top->bottom to decide and generate support structures.

For things we thought needed some fixing up, we wrote #TODO comments. 
