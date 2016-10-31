#a 3D point
class Point:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def print_point(self):
		print str(self.x)+" "+str(self.y)+" "+str(self.z)

	def point_tos(self):
		return str(self.x)+" "+str(self.y)+" "+str(self.z)

#consists of three Points
#and a point that has the highest z-coordinate
#and a point that has the lowest z-coordinate
class Triangle:
	def __init__(self, p1, p2, p3):
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3
		self.z_high = self.highest_z()
		self.z_low = self.lowest_z()

	def highest_z(self):
		if (self.p1.z >= self.p2.z):
			if (self.p1.z >= self.p3.z):
				return self.p1
			else:
				return self.p3
		else:
			if (self.p2.z >= self.p3.z):
				return self.p2
			else:
				return self.p3

	def lowest_z(self):
		if (self.p1.z <= self.p2.z):
			if (self.p1.z <= self.p3.z):
				return self.p1
			else:
				return self.p3
		else:
			if (self.p2.z <= self.p3.z):
				return self.p2
			else:
				return self.p3
	def print_triangle(self):
		print "triangle: " + self.p1.point_tos()
		print self.p2.point_tos()
		print self.p3.point_tos() + " trianglend"
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
for t in triangles:
	t.print_triangle()
	print





