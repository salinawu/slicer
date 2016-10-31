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
		print self.p1.point_tos()
		print self.p2.point_tos()
		print self.p3.point_tos()
		print 