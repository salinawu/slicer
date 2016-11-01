#!/usr/bin/python
from shapes import Point
from shapes import Triangle

#
# begin file parsing into points and eventually triangles
#
triangles = []

def parse_point(line):
	points = line.split()
	return Point(float(points[1]), float(points[2]), float(points[3]))

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
				i = i + 3
			else:
				i = i + 1

#calculates the intersection of 2 line segments, given by p1-p2 and p3-p4
def _calc_intersection(p1, p2, p3, p4, z):
	if (p4 == None):
		p4 = Point(p3.x+50, p3.y, p3.z)
		p3 = Point(p3.x-50, p3.y, p3.z)
	deltx1 = p2.x - p1.x
	delty1 = p2.y - p1.y
	deltx2 = p4.x - p3.x
	delty2 = p4.y - p3.y
	m1 = 0 if deltx1 == 0 else delty1/deltx1
	m2 = 0 if deltx2 == 0 else delty2/deltx2
	b1 = p1.y - m1*p1.x
	b2 = p3.y - m2*p3.x
	x = 0 if m1-m2 == 0 else (b2-b1)/(m1-m2)
	y = m1*x + b1
	return Point(x, y, z)

def calc_points():
	points = []
	#sorts triangles in ascending order by comparing lowest z-axis vertices
	sorted_triangles = sorted(triangles, key=lambda x: x.z_low.z, reverse=False)
	#a float for the lowest z to start slicing
	cur_z = sorted_triangles[0].z_low.z
	i = 0

	while i < len(sorted_triangles):
		triangle = sorted_triangles[i]

		#if one vertex is in the plane, ignore this triangle
		if (triangle.z_low.z == cur_z and triangle.find_other_point().z > cur_z):
			i = i + 1
		#other cases of triangle in the cutting plane
		elif (cur_z >= triangle.z_low.z and cur_z <= triangle.z_high.z):

			if (cur_z == triangle.p1.z):

				if (cur_z == triangle.p2.z):

					#all three points are in the plane
					if (cur_z == triangle.p3.z):
						points.append(triangle.p3)
					#p1, p2 are in the plane
					points.append(triangle.p2)

				#p1, p3 are in the plane
				elif (cur_z == triangle.p3.z):
					points.append(triangle.p3)

				#only p1 is in the plane
				else:
					points.append(_calc_intersection(triangle.z_high, triangle.z_low, triangle.p1, None, cur_z))


				points.append(triangle.p1)

			elif (cur_z == triangle.p2.z):

				#p2, p3 are in the plane
				if (cur_z == triangle.p3.z):
					points.append(triangle.p3)

				#only p2 is in the plane
				else:
					points.append(_calc_intersection(triangle.z_high, triangle.z_low, triangle.p2, None, cur_z))

				points.append(triangle.p2)

			#only p3 is in the plane
			elif (cur_z == triangle.p3.z):
				points.append(triangle.p3)
				points.append(_calc_intersection(triangle.z_high, triangle.z_low, triangle.p3, None, cur_z))

			#no vertices are in the plane, but the plane intersects the triangle
			else:
				other_p = triangle.find_other_point()
				points.append(_calc_intersection(triangle.z_low, other_p, triangle.z_low, triangle.z_high, cur_z))
				points.append(_calc_intersection(triangle.z_high, other_p, triangle.z_low, triangle.z_high, cur_z))

			i = i + 1

		#triangle is completely above the plane -- advance the plane
		elif (cur_z < triangle.z_low.z):
			cur_z = cur_z + 2 #2mm planes
	
		else:
			i = i + 1

	return points


parse_stl_file("cubetest.stl")
points = calc_points()
for p in points:
	p.print_point()
	print

