#!/usr/bin/python
from shapes import *
from contour_fill import *
from slicer import *
import copy

def cube_gcode(fill_density = 0.20, perimeter_layers = 2, thickness = 0.1):
    # run everything to get contour_segments populated:

    # parse the stl file so that we have all the triangles
    parse_stl_file("cubetest.stl")

    # calculate all the intersection points of all the triangles; store in a dictionary by plane (called lines)
    calc_points(thickness)

    # for each plane, remove all duplicate lines
    remove_dup_lines()

    # generates a dictionary of lists of perimeters (represented by lists of points) organized in planes
    perimeter_points = link_line_segments()

    # generates a dictionary of line segments to print out organized by plane
    contour_segments = fill_all_plane_contours(fill_density, perimeter_points)

    gcode = open('simpleCube.gcode', 'w+')

    gcode.write("M109 S207.000000\n")
    gcode.write(";Basic settings: Layer height:" + str(thickness) + " Wall layers:" + str(perimeter_layers) + "Fill:" + str(fill_density) + "\n")
    # TODO: gcode.write() the pre-printing stuff

    extruded = 0
    for plane in perimeter_points:
        perimeters = perimeter_points[plane]
        # first, loop through the perimeters and fill them in
        gcode.write(";Layer: " + str(plane) + "\n")
        for i in range(perimeter_layers):
            for ps in perimeters:
                gcode.write(";Printing perimeter\n")
                first = ps[0]
                gcode.write("G0 F1500 X"+ str(first.x) + " Y" + str(first.y) + " Z" + str(first.z) + "\n")
                for p in ps[1::]:
                    dist = p.dist_from_point(first)
                    x = str(p.x)
                    y = str(p.y)
                    z = str(p.z)
                    gcode.write("G1 X"+ x + " Y" + y + " E" + str(dist) + "\n")
                    extruded += dist
                    first = p

        gcode.write(";Printing inner fill\n")
        for line in contour_segments[plane]:
            head = line.p1
            tail = line.p2
            gcode.write("G0 F4200 X"+ str(head.x) + " Y" + str(head.y) + "\n")
            gcode.write("G1 F1500 X"+ str(tail.x) + " Y" + str(tail.y) + " E" + str(line.line_length()) + "\n")
            extruded += line.line_length()

    gcode.close()

cube_gcode()