import math
import sys

EPSILON = sys.float_info.epsilon

'''
Given two points, p1 and p2,
an x coordinate, x,
and y coordinates y3 and y4,
compute and return the (x,y) coordinates
of the y intercept of the line segment p1->p2
with the line segment (x,y3)->(x,y4)
'''
def yint(p1, p2, x, y3, y4):
	x1, y1 = p1
	x2, y2 = p2
	x3 = x
	x4 = x
	px = ((x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / \
		 float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
	py = ((x1*y2 - y1*x2)*(y3-y4) - (y1 - y2)*(x3*y4 - y3*x4)) / \
			float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3-x4))
	return (px, py)

'''
Given three points a,b,c,
computes and returns the area defined by the triangle
a,b,c.
Note that this area will be negative
if a,b,c represents a clockwise sequence,
positive if it is counter-clockwise,
and zero if the points are collinear.
'''
def triangleArea(a, b, c):
	return (a[0]*b[1] - a[1]*b[0] + a[1]*c[0] \
                - a[0]*c[1] + b[0]*c[1] - c[0]*b[1]) / 2.0;

'''
Given three points a,b,c,
returns True if and only if
a,b,c represents a clockwise sequence
(subject to floating-point precision)
'''
def cw(a, b, c):
	return triangleArea(a,b,c) < -EPSILON;
'''
Given three points a,b,c,
returns True if and only if
a,b,c represents a counter-clockwise sequence
(subject to floating-point precision)
'''
def ccw(a, b, c):
	return triangleArea(a,b,c) > EPSILON;

'''
Given three points a,b,c,
returns True if and only if
a,b,c are collinear
(subject to floating-point precision)
'''
def collinear(a, b, c):
	return abs(triangleArea(a,b,c)) <= EPSILON

'''
Given a list of points,
sort those points in clockwise order
about their centroid.
Note: this function modifies its argument.
'''
def clockwiseSort(points):
	# get mean x coord, mean y coord
	xavg = sum(p[0] for p in points) / len(points)
	yavg = sum(p[1] for p in points) / len(points)
	angle = lambda p:  ((math.atan2(p[1] - yavg, p[0] - xavg) + 2*math.pi) % (2*math.pi))
	points.sort(key = angle)
	#print(points)

def sort_by_x_coords(points):
	points.sort(key = lambda x: x[0])
	return points

def divide_half_by_x_coords(sorted_points):
	if len(sorted_points) > 6:
		m = len(sorted_points)//2
		while sorted_points[m-1][0] == sorted_points[m][0]:
			m += 1
		l = sorted_points[:m]
		r = sorted_points[m:]

		divide_half_by_x_coords(l)
		divide_half_by_x_coords(r)

		left_polygon = computeHull(l)
		right_polygon = computeHull(r)

		return merge(left_polygon,right_polygon)
	else:
		return base_case(sorted_points)

def base_case(sorted_points):
	if len(sorted_points) < 3:
		return sorted_points

	hull = set()
	for i in range(0,len(sorted_points)):
		for j in range(i+1, len(sorted_points)):
			count_ccw = 0
			count_cw = 0
			for k in range(0, len(sorted_points)):
				if ccw(sorted_points[i], sorted_points[j], sorted_points[k]):
					count_ccw += 1
				if cw(sorted_points[i], sorted_points[j], sorted_points[k]):
					count_cw += 1
			if count_ccw == 0 or count_cw == 0:
				hull.add(sorted_points[i])
				hull.add(sorted_points[j])
	hull = list(hull)
	clockwiseSort(hull)
	return hull

def merge(left,right):
	# Number of points of both polygons
    p1 = len(left)
    p2 = len(right)

	# Right most point of Polygon 1
    l = 0
    r = 0
    for point in range(1, p1):
        if left[point][0] > left[l][0]:
            l = point

    # Left most point of Polygon 2
    for point in range(1, p2):
        if right[point][0] < right[r][0]:
            r = point

	# Let's find the upper tanget
    upperLeft = l
    upperRight = r
    flag = False
    while flag == False:
        flag = True
        while cw(right[upperRight], left[upperLeft], left[(upperLeft + 1) % p1]) or collinear(right[upperRight], left[upperLeft], left[(upperLeft + 1) % p1]):
            upperLeft = (upperLeft + 1) % p1

        while ccw(left[upperLeft], right[upperRight], right[(p2 + upperRight - 1) % p2]) or collinear(left[upperLeft], right[upperRight], right[(p2 + upperRight - 1) % p2]):
            upperRight = (p2 + upperRight - 1) % p2
            flag = False

	# Let's find the lower tanget
    lowerLeft = l
    lowerRight = r
    flag = False
    while flag == False:
        flag = True
        while cw(left[lowerLeft], right[lowerRight], right[(lowerRight + 1) % p2]) or collinear(left[lowerLeft], right[lowerRight], right[(lowerRight + 1) % p2]):
            lowerRight = (lowerRight + 1) % p2

        while ccw(right[lowerRight], left[lowerLeft], left[(p1 + lowerLeft - 1) % p1]) or collinear(left[lowerLeft], right[lowerRight], right[(lowerRight + 1) % p2]):
            lowerLeft = (p1 + lowerLeft - 1) % p1
            flag = False

	# Finding the right and left tangents
    # to complete merge
    hull = []

    upperTan = upperLeft
    hull.append(left[upperLeft])
    while upperTan != lowerLeft:
        upperTan = (upperTan + 1) % p1
        hull.append(left[upperTan])

    lowerTan = lowerRight
    hull.append(right[lowerRight])
    while lowerTan != upperRight:
        lowerTan = (lowerTan + 1) % p2
        hull.append(right[lowerTan])

    return hull

'''
Replace the implementation of computeHull with a correct computation of the convex hull
using the divide-and-conquer algorithm
'''
def computeHull(points):
	sorted_points = sort_by_x_coords(points)
	return divide_half_by_x_coords(sorted_points)

if __name__ == '__main__':
	points = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(1,4)]
	print(computeHull(points))
	