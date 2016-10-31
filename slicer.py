from point import Point
from triangle import Triangle

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

parse_stl_file("cubetest.stl")
# for t in triangles:
# 	t.print_triangle()
# 	print

def slice():
	#sorts triangles in ascending order by comparing lowest z-axis vertices
	for triangle in sorted(triangles, cmp=lambda x,y: x > y, key= lambda x: x.z_low.z, reverse=False):

		triangle.print_triangle()






