# calculates all the normal vectors for a given triangle
# made up of three vectors
class Point:

    def __init__(
        self,
        x,
        y,
        z,
        ):
        self.x = x
        self.y = y
        self.z = z

    def is_equal(self, other):
    	return self.x == other.x and self.y == other.y and self.z == other.z

    def print_point(self):
        print str(self.x) + ' ' + str(self.y) + ' ' + str(self.z)

    def point_tos(self):
        return str(self.x) + ' ' + str(self.y) + ' ' + str(self.z)

# consists of three Points
# and a point that has the highest z-coordinate
# and a point that has the lowest z-coordinate

class Triangle:

    def __init__(
        self,
        p1,
        p2,
        p3,
        ):

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.z_high = self.highest_z()
        self.z_low = self.lowest_z()

    def return_points(self):
        return [self.p1, self.p2, self.p3]

    def highest_z(self):
        if self.p1.z >= self.p2.z:
            if self.p1.z >= self.p3.z:
                return self.p1
            else:
                return self.p3
        else:
            if self.p2.z >= self.p3.z:
                return self.p2
            else:
                return self.p3

    def lowest_z(self):
        if self.p1.z <= self.p2.z:
            if self.p1.z <= self.p3.z:
                return self.p1
            else:
                return self.p3
        else:
            if self.p2.z <= self.p3.z:
                return self.p2
            else:
                return self.p3

    # returns the other point that is not the z_high or z_low

    def find_other_point(self):
        if (not self.z_high.is_equal(self.p1)) and (not self.z_low.is_equal(self.p1)):
            return self.p1
        elif (not self.z_high.is_equal(self.p2)) and (not self.z_low.is_equal(self.p2)):
            return self.p2
        else:
            return self.p3

    def print_triangle(self):
        print self.p1.point_tos()
        print self.p2.point_tos()
        print self.p3.point_tos()
        print

class Line():

    def __init__(self, p1, p2, z):
        self.p1 = p1
        self.p2 = p2
        self.z = z

    def same_line(self, l):
        return self.p1.is_equal(l.p1) and self.p2.is_equal(l.p2)
