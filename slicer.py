#!/usr/bin/python
from shapes import *
from contour_fill import *
import copy

#
# begin file parsing into points and eventually triangles and then line segments
#
triangles = []

# this is the dict of perimeter lines; each key corresponds to a z-axis plane
# and the values are the line segments
lines = {}

# this is the dict of segments representing fill space; i.e. what needs to be converted to g-code
# keys represent z-axis planes, each with line segments
contour_segments = {}

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

#calculates the intersection of 2 line segments, given by p1-p2 and p3-p4
def _calc_intersection(p1, p2, p3, p4, z):
	if (p4 == None):
		p4 = Point(p3.x+50, p3.y, p3.z)
		p3 = Point(p3.x-50, p3.y, p3.z)
	deltx1 = p2.x - p1.x
	delty1 = p2.y - p1.y
	deltx2 = p4.x - p3.x
	delty2 = p4.y - p3.y
	m1 = 0 if not deltx1 else delty1/deltx1
	m2 = 0 if not deltx2 else delty2/deltx2
	b1 = p1.y - m1*p1.x
	b2 = p3.y - m2*p3.x
	x = 0 if not m1-m2 else (b2-b1)/(m1-m2)
	y = m1*x + b1
	return Point(x, y, z)

def calc_points(max_z, thickness):
	points = []
	#sorts triangles in ascending order by comparing lowest z-axis vertices
	sorted_triangles = sorted(triangles, key=lambda x: x.z_low.z, reverse=False)

	#TODO: DETERMINE WHAT MIN Z TO START AT
	# shouldn't it be 0?
	for plane in range(-10, max_z, thickness):
		lines[plane] = []
		for t in triangles:
			if triangle_intersects_plane(t, plane):
				# calculate the intersecting points and calculate the correponding line segments
				intersection_case(t, plane, points)

def triangle_intersects_plane(t, plane):
	return t.z_low.z <= plane <= t.z_high.z

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
	elif triangle.z_low.z < otherpt.z < triangle.z_high:
		if otherpt.z==plane:
			intersection_pt = _calc_intersection(triangle.z_low, triangle.z_high, otherpt, None, plane)
			points.append(otherpt)
			points.append(intersection_pt)
			lines[plane] += calc_line_segments([otherpt, intersection_pt], -1)
		elif triangle.find_other_point().z > plane:
			# save 2 intersection points
			i1 = _calc_intersection(triangle.z_low, triangle.z_high, otherpt, None, plane)
			i2 = _calc_intersection(triangle.z_low, otherpt, otherpt, None, plane)
			points.append(i1)
			points.append(i2)
			lines[plane] += calc_line_segments([i1, i2], -1)
		else:
			i1 = _calc_intersection(triangle.z_low, triangle.z_high, otherpt, None, plane)
			i2 = _calc_intersection(otherpt, triangle.z_high, otherpt, None, plane)
			points.append(i1)
			points.append(i2)
			lines[plane] += calc_line_segments([i1, i2], -1)

	# case 5: don't do anything

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
	for plane in lines.keys():
		# l is each line in the corresponding plane
		for l in lines[plane]:
			exclude_self = lines[plane]
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
	points = [] #list of list of points to be returned
	for plane in lines:
		exclude_lines = lines[plane]
		#if no lines in the plane, we skip
		if not exclude_lines:
			continue
		points_list = []
		while True:
			line = exclude_lines[0]
			start_point = line.p1
			point2 = None
			points_list.append(start_point)
			if len(exclude_lines) <= 1:
				break

			while not start_point.is_equal(point2):
				exclude_self = copy.copy(exclude_lines)
				exclude_self.remove(line)
				for line2 in exclude_self:
					if line.p2.is_equal(line2.p1):
						points_list += [line.p2, line2.p2]
						exclude_lines.remove(line)
						line = line2
						point2 = line2.p2
						break	
					elif line.p2.is_equal(line2.p2):
						points_list += [line.p2, line2.p1]
						exclude_lines.remove(line)
						line = line2
						point2 = line2.p1
						break
		points.append(points_list)

	return points

# fill in the contours from the perimeters for each plane
def fill_all_plane_contours(density):
	for plane, ls in lines:
		contour_segments[plane] = contour_fill(perimeters, ls, density, 'horizontal')
		contour_segments[plane] += contour_fill(perimeters, ls, density, 'vertical')

# at this point, contour_segments should be a dictionary of planes, each plane populated with a single array of
# line segments representing what must be filled at that level, horizontal segments and then vertical segments 

parse_stl_file("cubetest.stl")
calc_points(10, 10)
remove_dup_lines()
perimeter = link_line_segments()
for p in perimeter:
	print p

