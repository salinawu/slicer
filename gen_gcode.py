#!/usr/bin/python
from shapes import *
from contour_fill import *
import copy

def cube_gcode(fill_density = 0.20, perimeter_layers = 2, thickness = 0.1):
    # run everything to get contour_segments populated
    parse_stl_file("cubetest.stl")
    calc_points(thickness)
    remove_dup_lines()
    
    gcode = open('cube.gcode', 'w+')

    gcode.write("M109 S207.000000")
    gcode.write(";Basic settings: Layer height: 0.1 Walls: 0.8 Fill: " + str(fill_density))

    contour_segments
