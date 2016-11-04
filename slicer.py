#!/usr/bin/python
from shapes import Point
from shapes import Triangle
from shapes import Line

#
# begin file parsing into points and eventually triangles and then line segments
#
triangles = []
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
		lines = f.readlines()
		length = len(lines)
		i = 0
		while i < length:
			line = lines[i]
			p1 = None
			if "vertex" in line:
				p1 = parse_point(line)
				line = lines[i+1]
				p2 = parse_point(line)
				line = lines[i+2]
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

	for plane in range(0, max_z, thickness):
		lines[plane] = []
		for t in triangles:
			if triangle_intersects_plane?(t, plane):
				# return the intersecting points and calculate the correponding line segments
				points = intersection_case(triangle, plane, points)
	return points

def triangle_intersects_plane?(t, plane):
	return t.z_low.z <= plane <= t.z_high.z

def intersection_case(triangle, plane, points):
	z1 = triangle.p1.z
	z2 = triangle.p2.z
	z3 = triangle.p3.z

	# case 1: all points on the plane; save all points
	if z1==z2==z3:
		points += [i for i in triangle.return_points()]
		lines[plane] += calc_line_segments([i for i in triangle.return_points()], -2)

	# case 2: two points on the plane; save 2 points on the plane
	elif triangle.z_low.z == triangle.find_other_point().z == plane:
		points += [triangle.z_low, triangle.find_other_point()]
		lines[plane] += calc_line_segments([triangle.z_low, triangle.find_other_point()], triangle.z_high)
	elif triangle.z_high.z == triangle.find_other_point().z == plane:
		points += [triangle.z_high, triangle.find_other_point()]
		lines[plane] += calc_line_segments([triangle.z_low, triangle.find_other_point()], triangle.z_low)

	# case 3: save point on the plane and where the other intersection point is
	elif triangle.z_low.z < triangle.find_other_point().z < triangle.z_high:
		if triangle.find_other_point().z==plane:
			intersection_pt = _calc_intersection(triangle.z_low, triangle.z_high, triangle.find_other_point(), None, plane)
			points.append(triangle.find_other_point())
			points.append(intersection_pt)
			lines[plane] += calc_line_segments([triangle.find_other_point(), intersection_pt], -1)
		elif triangle.find_other_point().z > plane:
			# save 2 intersection points
			i1 = _calc_intersection(triangle.z_low, triangle.z_high, triangle.find_other_point(), None, plane)
			i2 = _calc_intersection(triangle.z_low, triangle.find_other_point(), triangle.find_other_point(), None, plane)
			points.append(i1)
			points.append(i2)
			lines[plane] += calc_line_segments([i1, i2], -1)
		else:
			i1 = _calc_intersection(triangle.z_low, triangle.z_high, triangle.find_other_point(), None, plane)
			i2 = _calc_intersection(triangle.find_other_point(), triangle.z_high, triangle.find_other_point(), None, plane)
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
			exclude_self = lines[plane].remove(l)
			# find all the lines identical to the one we're currently looking at
			same_lines = [x if l.same_line?(x) for x in exclude_self]
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

parse_stl_file("cubetest.stl")
points = calc_points()
for p in points:
	p.print_point()
	print
