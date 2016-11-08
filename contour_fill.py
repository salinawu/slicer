#!/usr/bin/python
from shapes import *
import numpy as np
import pdb

# takes in a list of a list of points (list of perimeters), list of list of lines, desired fill density,
# and direction (horizontal vs vertical)
# returns the line segments to be filled out
# ideally, this function should be abstracted to work on two axes
def contour_fill(perimeters, lines, density, direction):
    # not looking at z axis for any of these points
    flatten_list = lines #sum(lines, [])

    # sort perimeters by minimum x or y so that this is a list of concentric perimeters starting from the outermost layer
    perimeters.sort(key=lambda l:min(l, key=lambda p:p.y)) if direction == 'horizontal' else perimeters.sort(key=lambda l:min(l, key=lambda p:p.x))

    # look at the first perimeter because we sorted by outermost layer
    max_val = max(perimeters[0], key=lambda y: y.y).y if direction == 'horizontal' else  max(perimeters[0], key=lambda y: y.x).x
    min_val = min(perimeters[0], key=lambda y: y.y).y if direction == 'horizontal' else  min(perimeters[0], key=lambda y: y.x).x

    if max_val == min_val:
        return []

    line_segments = []
    # density should be a percentage; e.g. 20% or 0.20
    step = (max_val - min_val) / density
    for y in np.arange(min_val, max_val+step, step):
        intersections = find_intersections(flatten_list, y, direction)
        num_segs = len(intersections)
        # if num_segs % 2 != 0:
        #     print num_segs
        for i in range(0, num_segs, 2):
            # append only even to odd intersection points
            if i+1 < num_segs: 
                line_segments.append(Line(intersections[i], intersections[i+1], intersections[i+1].z))
    return line_segments


# find the intersections between a horizontal or vertical line and a list of lines
def find_intersections(lines, y, direction):
    # case 1: intersects the perimeter at two non-end locations (normal; somewhere in the middle of the perimeter)
    # case 2: intersects the perimeter at two end locations
        # subcase a: intersections are dictinct; keep them both
        # subcase b: intersections are the same; discard both
    # case 3: completely horizontal (for y lines) or vertical (for x line)
        # ignore (this would be a perimeter; we're already filling out the perimeters)
    intersection_points = []
    for i in lines:
        slope = i.slope()

        # case 3
        if (slope == 0 and direction == 'horizontal') or (slope == float("inf") and direction == 'vertical'):
            next
            # if (i.p1.y == y and direction == 'horizontal') or (i.p1.x==y and direction == 'vertical'): 
            #     intersection_points.append(i.p1)
            #     intersection_points.append(i.p2)

        intersection = i.horizontal_intersection(y) if direction == 'horizontal' else i.vertical_intersection(y)
        if intersection:
            same_points = [x for x in intersection_points if x.is_equal(intersection)]
            if same_points:
                # case 2 subcase b
                intersection_points = [x for x in intersection_points if x not in same_points]
            else:
                # case 1 and case 2 subcase a
                intersection_points.append(intersection)

    intersection_points.sort(key=lambda p:p.x) if direction == 'horizontal' else intersection_points.sort(key=lambda p:p.y)
    # order list and return
    # TODO something is wrong...

    return intersection_points
