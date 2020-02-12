import math
import sys
import logging
from random import randint as r

EPSILON = sys.float_info.epsilon

logging.basicConfig(level=logging.INFO, format="%(name)s:%(module)s.%(funcName)s:%(message)s")

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

def sort_by_x_coords(points):
	points.sort(key = lambda x: x[0])
	return points

def divide_half_by_x_coords(points):
	if len(points) > 5:
		m = len(points)//2
		#logging.info(m)
		# print(points[m-1][0])
		#print(points[m])
		while points[m-1][0] == points[m][0]:
			m += 1
			#print(m)
		l = points[:m].copy()
		#logging.info(l)

		r = points[m:].copy()
		#logging.info(r)
		divide_half_by_x_coords(l)
		divide_half_by_x_coords(r)

		# logging.info(r)
		#logging.info(points)

		#divide_half_by_x_coords(r)
		#computeHull(points)
	# else:
	# 	logging.info(points)

# def base_case(points):

'''
Replace the implementation of computeHull with a correct computation of the convex hull
using the divide-and-conquer algorithm
'''
def computeHull(points):
	return points

if __name__ == '__main__':

	points = [(2,3),(3,4),(3,5),(5,6),(5,7),(5,8),(5,9),(6,8)]
	# points = [(2,3),(2,4),(3,5),(5,6),(5,7),(5,8)]
	# for i in range(0,6):
	# 	x1 = r(1,3)
	# 	y1 = r(1,3)
	# 	point = (x1,y1)
	# 	points.append(point)
	points = sort_by_x_coords(points)
	#print(points)

	divide_half_by_x_coords(points)
	#computeHull(points)