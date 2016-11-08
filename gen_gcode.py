#!/usr/bin/python
from shapes import *
from contour_fill import *
from slicer import *
import copy

def cube_gcode(filename, outputfilename, fill_density = 20, perimeter_layers = 2, thickness = 1):
    # run everything to get contour_segments populated:

    # parse the stl file so that we have all the triangles
    parse_stl_file(filename)

    # calculate all the intersection points of all the triangles; store in a dictionary by plane (called lines)
    calc_points(thickness)

    # for each plane, remove all duplicate lines
    remove_dup_lines()

    # generates a dictionary of lists of perimeters (represented by lists of points) organized in planes
    perimeter_points = link_line_segments()

    # generates a dictionary of line segments to print out organized by plane
    contour_segments = fill_all_plane_contours(fill_density, perimeter_points)
    print len(contour_segments)
    print len(perimeter_points)

    gcode = open(outputfilename, 'w+')

    # opening gcode
    gcode.write("M109 S207.000000\n")
    gcode.write(";Basic settings: Layer height: " + str(thickness) + " Wall layers: " + str(perimeter_layers) + " Fill: " + str(fill_density) + "\n")
    gcode.write(";M190 S70 ;Uncomment to add your own bed temperature line\n\
G21        ;metric values\n\
G90        ;absolute positioning\n\
M82        ;set extruder to absolute mode\n\
M107       ;start with the fan off\n\
G28 X0 Y0  ;move X/Y to min endstops\n\
G28 Z0     ;move Z to min endstops\n\
G29        ;Run the auto bed leveling\n\
;G1 Z15.0 F4200 ;move the platform down 15mm\n\
G92 E0                  ;zero the extruded length\n\
G1 F200 E3              ;extrude 3mm of feed stock\n\
G92 E0                  ;zero the extruded length again\n\
G1 F4200\n\
M117 Printing...\n")

    extruded = 0

    for index, plane in enumerate(sorted(perimeter_points)):
        perimeters = perimeter_points[plane]
        # first, loop through the perimeters and fill them in
        gcode.write(";Layer: " + str(index) + "\n")
        if index==0:
            gcode.write("M107\n")
        elif index==1:
            gcode.write("M106 S127\n")
        elif index==2:
            gcode.write("M106 S255\n")

        for i in range(perimeter_layers):
            for ps in perimeters:
                # print len(ps)

                gcode.write(";Printing perimeter\n")
                first = ps[0]
                gcode.write("G0 F1500 X"+ str(first.x) + " Y" + str(first.y) + " Z" + str(first.z) + "\n")
                for p in ps[1::]:
                    dist = p.dist_from_point(first)
                    x = str(p.x)
                    y = str(p.y)
                    z = str(p.z)
                    gcode.write("G1 X"+ x + " Y" + y + " E" + str(extruded + dist) + "\n")
                    extruded += dist
                    first = p

        gcode.write(";Printing inner fill\n")
        for line in contour_segments[plane]:
            head = line.p1
            tail = line.p2
            gcode.write("G0 F4200 X"+ str(head.x) + " Y" + str(head.y) + "\n")
            gcode.write("G1 F1500 X"+ str(tail.x) + " Y" + str(tail.y) + " E" + str(extruded + line.line_length()) + "\n")
            extruded += line.line_length()

    # closing gcode
    gcode.write(";End GCode\n\
M104 S0                     ;extruder heater off\n\
M140 S0                     ;heated bed heater off (if you have it)\n\
G91                                    ;relative positioning\n\
G1 E-1 F300                            ;retract the filament a bit before lifting the nozzle, to release some of the pressure\n\
G1 Z+0.5 E-5 X-20 Y-20 F4200 ;move Z up a bit and retract filament even more\n\
G28 X0 Y0                              ;move X/Y to min endstops, so the head is out of the way\n\
M84                         ;steppers off\n\
G90                         ;absolute positioning")

    gcode.close()

# cube_gcode("cubetest20.stl", "simpleCube.gcode")
# cube_gcode("cylindertest.stl", "simpleCylinder.gcode")

# cube_gcode("cube.stl", "cube.gcode")
cube_gcode("cylinder.stl", "cylinder.gcode")
