from point import Point
from triangle import Triangle

high = Point(0,0,4)
low = Point(0,0,-1)
we = Point(0,0,3)

tri = Triangle(high,low,we)
print "high: " + tri.z_high.point_tos() + " expected: 0 0 4"
print "low: " + tri.z_low.point_tos() + " expected: 0 0 -1"

tri2 = Triangle(low,high,we)
print "high: " + tri2.z_high.point_tos() + " expected: 0 0 4"
print "low: " + tri2.z_low.point_tos() + " expected: 0 0 -1"
 
tri3 = Triangle(we,high,low)
print "high: " + tri3.z_high.point_tos() + " expected: 0 0 4"
print "low: " + tri3.z_low.point_tos() + " expected: 0 0 -1"

tri4 = Triangle(we,low, high)
print "high: " + tri4.z_high.point_tos() + " expected: 0 0 4"
print "low: " + tri4.z_low.point_tos() + " expected: 0 0 -1"

tri5 = Triangle(high,we,low)
print "high: " + tri5.z_high.point_tos() + " expected: 0 0 4"
print "low: " + tri5.z_low.point_tos() + " expected: 0 0 -1"

tri6 = Triangle(low,we,high)
print "high: " + tri6.z_high.point_tos() + " expected: 0 0 4"
print "low: " + tri6.z_low.point_tos() + " expected: 0 0 -1"