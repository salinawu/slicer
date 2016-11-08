#!/usr/bin/python
from shapes import *
from contour_fill import *
from collections import defaultdict
import copy
import numpy as np

#
# begin file parsing into points and eventually triangles and then line segments
#
triangles = []

# this is the dict of perimeter lines; each key corresponds to a z-axis plane
# and the values are the line segments
lines = {}

# takes in a line from a file of the form 'vertex x y z' and returns the point corresponding to it
def parse_point(line):
	points = line.split()
	if points and points[0] == 'vertex':
		return Point(float(points[1]), float(points[2]), float(points[3]))
	else:
		raise NameError('Line cannot be parsed into a point')

# stores all the triangles from an stl file into global array of triangles
def parse_stl_file(filename):
	with open(filename, 'r') as f:
		filelines = f.readlines()
		length = len(filelines)
		i = 0
		while i < length:
			line = filelines[i]
			p1 = None
			if "vertex" in line:
				p1 = parse_point(line)
				line = filelines[i+1]
				p2 = parse_point(line)
				line = filelines[i+2]
				p3 = parse_point(line)
				triangles.append(Triangle(p1, p2, p3))
				i += 3
			else:
				i += 1

#parse_stl_file("cubetest.stl")

#calculates the intersection of a line <p1,p2> and a plane in 3D
def calc_intersection(p1, p2, z):
	plane = Plane(Point(0,0,z), Vector(0,0,1))
	vector = Vector(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
	return plane.line_intersection(vector, p1)

# loops through each plane and triangle, finds the points of intersections
# will populate lines dictionary (by way of intersection_case())
def calc_points(thickness):
	points = []
	#sorts triangles in ascending order by comparing lowest z-axis vertices
	sorted_triangles = sorted(triangles, key=lambda x: x.z_low.z)

	min_z = sorted_triangles[0].z_low.z
	max_z = max(triangles, key=lambda x: x.z_high.z).z_high.z

	for plane in np.arange(min_z, max_z+thickness, thickness):
		lines[plane] = []
		for t in triangles:
			if t.intersects_plane(plane):
				# calculate the intersecting points and calculate the correponding line segments
				intersection_case(t, plane, points)

# for each intersection, store the line segments (unrefined perimeters)
def intersection_case(triangle, plane, points):
	z1 = triangle.p1.z
	z2 = triangle.p2.z
	z3 = triangle.p3.z
	otherpt = triangle.find_other_point()

	# case 1: all points on the plane; save all points
	if z1==z2==z3:
		points += [i for i in triangle.return_points()]
		lines[plane] += calc_line_segments([i for i in triangle.return_points()], -2)

	# case 2: two points on the plane; save 2 points on the plane
	elif triangle.z_low.z == otherpt.z == plane:
		points += [triangle.z_low, otherpt]
		lines[plane] += calc_line_segments([triangle.z_low, otherpt], triangle.z_high)
	elif triangle.z_high.z == otherpt.z == plane:
		points += [triangle.z_high, otherpt]
		lines[plane] += calc_line_segments([triangle.z_low, otherpt], triangle.z_low)

	# case 3: save point on the plane and where the other intersection point is
	elif triangle.z_low.z <= otherpt.z <= triangle.z_high.z:
		# case 5: don't do anything
		if (otherpt.z != triangle.z_low.z and triangle.z_low.z == plane) or (otherpt.z != triangle.z_high.z and triangle.z_high.z == plane):
			return

		if otherpt.z==plane:
			intersection_pt = calc_intersection(triangle.z_low, triangle.z_high, plane)
			points.append(otherpt)
			points.append(intersection_pt)
			lines[plane] += calc_line_segments([otherpt, intersection_pt], -1)
		elif otherpt.z > plane:
			# save 2 intersection points
			i1 = calc_intersection(triangle.z_low, triangle.z_high, plane)
			i2 = calc_intersection(triangle.z_low, otherpt, plane)
			points.append(i1)
			points.append(i2)
			lines[plane] += calc_line_segments([i1, i2], -1)
		else:
			i1 = calc_intersection(triangle.z_low, triangle.z_high, plane)
			i2 = calc_intersection(triangle.z_high, otherpt, plane)
			points.append(i1)
			points.append(i2)
			lines[plane] += calc_line_segments([i1, i2], -1)

# calculate the line segments based on a list of 2 or 3 points as well as the corresponding z value
def calc_line_segments(ps, z):
	length = len(ps)
	if length==2:
		return [Line(ps[0], ps[1], z)]
	elif length==3:
		return [Line(ps[0], ps[1], z), Line(ps[2], ps[1], z), Line(ps[2], ps[0], z)]
	else:
		raise NameError('can only have 2 or 3 points')

def remove_dup_lines():
	# plane is the z value of each plane
	for plane in lines:
		# l is each line in the corresponding plane
		for l in lines[plane]:
			exclude_self = copy.copy(lines[plane])
			exclude_self.remove(l)
			# find all the lines identical to the one we're currently looking at
			same_lines = [x for x in exclude_self if l.same_line(x)]
			for same in same_lines:
				# we might have already taken out the line in contention
				if l not in lines[plane]:
					break
				remove_line_segments(l, same, plane)

# uses algo from paper to determine whether we should remove 1 or both line segments
# should only arrive here if l1==l2
def remove_line_segments(l1, l2, plane):
	if (l1.z == l2.z == -2) or (l1.z > plane and l2.z > plane) or (l1.z < plane and l2.z < plane):
		lines[plane].remove(l1)
		lines[plane].remove(l2)
	elif (l1.z == -2 and l2.z != -2) or (l1.z != -2 and l2.z == -2) or (l1.z > plane and l2.z < plane) or (l1.z < plane and l2.z > plane):
		 lines[plane].remove(l2)
	else:
		raise NameError('should never end up in this case')

def link_line_segments():
	# points = {} #dictionary of a list of list of points to be returned
	# for plane in lines:
	# 	#exclude_lines is the line segments of the perimeters
	# 	exclude_lines = copy.copy(lines[plane])
	# 	#if no lines in the plane, we skip
	# 	if not exclude_lines:
	# 		continue
	# 	points_list = []
	# 	print plane
	# 	#while there are line segments remaining: 
	# 	while len(exclude_lines) > 0:
	# 		perimeter = []

	# 		#take a random item from the list
	# 		line = exclude_lines[0]
	# 		start_point = line.p1 #the point we must get back to
	# 		point2 = line.p2 #the point we use to trace the perimeter
	# 		perimeter += [line.p1, line.p2]

	# 		exclude_lines.remove(line)

	# 		for l in exclude_lines: 
	# 			if l.p1.is_equal(point2): 
	# 				perimeter.append(l.p2)
	# 				point2 = l.p2
	# 				exclude_lines.remove(l)
	# 				if l.p2 == start_point: 
	# 					break 
	# 			elif l.p2.is_equal(point2): 
	# 				perimeter.append(l.p1)
	# 				point2 = l.p1
	# 				exclude_lines.remove(l)
	# 				if l.p1 == start_point: 
	# 					break
	# 			print "here" 
	# 		print len(perimeter)
	# 		points_list.append(perimeter)
	# 	points[plane] = points_list

	# return points
	
	points = {} #dictionary of a list of list of points to be returned
	for plane in lines:
		exclude_lines = copy.copy(lines[plane])
		#if no lines in the plane, we skip
		if not exclude_lines:
			continue
		points_list = []
		while len(exclude_lines) > 1:
			perimeter = []
			line = exclude_lines[0]
			start_point = line.p1 #the point we must get back to
			point2 = line.p2 #the point we use to trace the perimeter
			perimeter.append(start_point)
			exclude_self = copy.copy(exclude_lines)
			exclude_self.remove(line)

			while not start_point.is_equal(point2) or len(exclude_lines) == 0:

				exclude_self = copy.copy(exclude_lines)
				exclude_self.remove(line)

				for line2 in exclude_self:
					if line2.contains(point2):
						#line2.p2 is the point to be compared next
						if line2.p1.is_equal(point2):
							perimeter += [line.p2, line2.p2]
							point2 = line2.p2
						#line2.p1 is the point to be compared next
						else:
							perimeter += [line.p2, line2.p1]
							point2 = line2.p1
						exclude_lines.remove(line)
						line = line2

			points_list.append(perimeter)
			
		points[plane] = points_list

	return points

# fill in the contours from the perimeters for each plane
def fill_all_plane_contours(density, points):
	# this is the dict of segments representing fill space; i.e. what needs to be converted to g-code
	# keys represent z-axis planes, each with line segments
	contour_segments = {}
	for plane in lines:
		# list of a list of points (representing a list of perimeters)
		ps = points[plane]
		# list of line segments on each plane
		ls = lines[plane] 
		contour_segments[plane] = contour_fill(ps, ls, density, 'horizontal')
		contour_segments[plane] += contour_fill(ps, ls, density, 'vertical')
	return contour_segments

# at this point, contour_segments should be a dictionary of planes, each plane populated with a single array of
# line segments representing what must be filled at that level, horizontal segments and then vertical segments
