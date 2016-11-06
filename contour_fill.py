#!/usr/bin/python
from shapes import Point
from shapes import Triangle
from shapes import Line

# takes in a list of a list of points (list of perimeters)
# returns the line segments to be filled out
# ideally, this function should be abstracted to work on two axes
def contour_fill(perimeters, lines, density):
    # not looking at z axis for any of these points
    # for now, look at y axis.

    # sort by maximum y so that this is a list of concentric perimeters starting from the outermost layer
    perimeters.sort(key=lambda l:max(l.y), reverse=True)

    # look at the first perimeter because we sorted by outermost layer
    max_y = max(perimeters[0], key=lambda y: y.y)
    min_y = min(perimeters[0], key=lambda y: y.y)

    line_segments = []
    # density should be a percentage; e.g. 20% or 0.20
    step = (max_y - min_y) * density
    for y in range(min_y, max_y+step, step):
        intersections = find_intersections(lines, y)
        num_segs = len(line_segments)
        if num_segs % 2 != 0:
            raise NameError('should have an even number of intersections')
        for i in range(0, num_segs, 2):
            # append only even to odd intersection points
            line_segments.append(intersections[i], intersections[i+1])

    return line_segments


# find the intersections between a y axis and a list of lines
def find_intersections(lines, y):
    # case 1: intersects the perimeter at two non-end locations (normal; somewhere in the middle of the perimeter)
    # case 2: intersects the perimeter at two end locations
        # subcase a: intersections are dictinct; keep them both
        # subcase b: intersections are the same; discard both
    # case 3: completely horizontal. ignore (this would be a perimeter; we're already filling out the perimeters)

    intersection_points = []
    for i in lines:
        slope = i.slope()

        # case 3
        if slope == 0:
            continue

        intersection = i.horizontal_intersection(y)
        if intersection:
            if intersection in intersection_points:
                # case 2 subcase b
                intersection_points.remove(intersection)
            else:
                # case 1 and case 2 subcase a
                intersection_points.append(intersection)

    # order list and return
    return intersection_points.sort(key = lambda p: p.x)
