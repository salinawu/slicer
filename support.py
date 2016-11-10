from shapes import *

#returns pm1 if pm1 >= pm2, pm2 otherwise
def bigger_perimeter(pm1, pm2):
	if pm2 == None and pm1 != None:
		return pm1
	elif pm1 == None and pm2 != None:
		return pm2

	for p1 in pm1.pm:
		for p2 in pm2.pm:
			if p2.x > p1.x or p2.y > p1.y:
				return pm2
	return pm1

#returns True if pm1 < pm2, False otherwise
def is_smaller_perimeter(pm1, pm2):
	if pm2 == None:
		return False
	bb_pm1 = find_bounding_box(pm1)
	bb_pm2 = find_bounding_box(pm2)
	print "top: " + str(bb_pm1[0].y) + " " + str(bb_pm2[0].y)
	print "bottom: "  + str(bb_pm1[1].y) + " " + str(bb_pm2[1].y)
	print "left: " + str(bb_pm1[2].x)+ " " + str(bb_pm2[2].x)
	print "right: "  + str(bb_pm1[3].x) + " " + str(bb_pm2[3].x)
	return bb_pm1[0].y < bb_pm2[0].y and bb_pm1[1].y > bb_pm2[1].y and bb_pm1[2].x > bb_pm2[2].x and bb_pm1[3].x < bb_pm2[3].x

def find_bounding_box(pm):
	top = pm[0]
	bottom = pm[0]
	left = pm[0]
	right = pm[0]
	for pt in pm:
		if pt.x < left.x:
			left = pt
		if pt.x > right.x:
			right = pt
		if pt.y < bottom.y:
			bottom = pt
		if pt.y > top.y:
			top = pt
	top_left = Point(top.y, left.x, top.z)
	bottom_left = Point(bottom.y, left.x, bottom.z)
	top_right = Point(top.y, right.x, top.z)
	bottom_right = Point(bottom.y, right.x, bottom.z)
	return [top, bottom, left, right, top_left, top_right, bottom_right, bottom_left]

def change_bounding_box(bounding_box, height):
	to_ret = []
	for pt in bounding_box:
		to_ret.append(Point(pt.x, pt.y, height))
	return to_ret

def calc_support(perimeters):
	cur_max = Perimeter(None, None)
	support = {}
	size = len(perimeters)
	keys = perimeters.keys()
	keys.sort()

	#goes through the planes in descending order
	for plane in sorted(perimeters, reverse=True):
		lines = perimeters[plane]
		support[plane] = []
		print plane

		if len(lines) == 0:
			continue
		#finds the outter perimteter in the list of perimeters
		outter_pms = []
		for ls in lines:
			outter_pms.extend(ls)
		outter_pm = Perimeter(outter_pms, plane)

		#determines if the current perimeter is smaller than the max perimeter
		if is_smaller_perimeter(outter_pm.pm, cur_max.pm):
			print "min"
			support[plane].append(outter_pm.pm)
		# the current perimeter is bigger than the current max perimeter
		else:
			print "max"
			cur_max = outter_pm

	bounding_box = find_bounding_box(cur_max.pm)

	#makes a list of list of perimeters
	for plane in support:
		if len(support[plane]) == 0:
			continue
		support[plane][0].extend(change_bounding_box(bounding_box, plane))

	return support





