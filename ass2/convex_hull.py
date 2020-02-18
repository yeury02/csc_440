import math
import sys
'''
Algorithm Invarient

Definition - Let S be a list of tuples corresding to points in a 2-D plane.
	        The goal is to get the smallest set of points that make a Convex Hull
   	        and return the list in clock wise order. Remember, a set of points is 
	        defined as the smallest convex polygon, that encloses all of the points 
	        in the set. Convex means that the polygon has no corner that is bent inwards.

Initialization (base case) - any set of points less than 3 is itself hull. Remember a 
		                    polygon has to have at least 3 points to make a polygon. 
		                    For example: an empty S would result in an empty hull, same goes for 1 or
			                two points
		                    if there are between 3-5 points, a Gift Wrapping algorithm is implemented:
		                    computes the convex hull on small inputs, it is faster than brute force
		                    in fact, the complexity is O(nh) where n is the input size = S and h is the
		                    hull size

Maintance (Induction Step) - Assuming S is true for each divide step, this step is done 
			                recursively until it hits the base case. Imagine having S
			                amount of points sorted by x-coords and being sub-divided into "halfs" everytime,
			                and once it reaches the base case, the hull gets computed going
			                up the tree and computing the hull each step of the way. Until
			                it has the hull for from both halfs.

                            The fun part comes in the merging: Goals is to find the upper,lower,left,right tanget
                            - Left - pick highest x value
                            - right - pick lowest x value
                            - find the y intercept, move left counter clockwise and right clockwise, do this repreately 
                                until you find highest y-intercept
                            - do the same for lower tanget but instead reverse the work
                            if the base case is true, then we assume this is also true, which leads us to getting the 
                            smallest set of convex hull

Termination - This algorithm terminates when it is done making comparisons to find the upper tangest, lower tangets, etc.
		      Then returns the smallest set of points in clockwise order that make up the convex hull
'''

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
                - a[0]*c[1] + b[0]*c[1] - c[0]*b[1]) / 2.0

'''
Given three points a,b,c,
returns True if and only if 
a,b,c represents a clockwise sequence
(subject to floating-point precision)
'''
def cw(a, b, c):
	return triangleArea(a,b,c) < -EPSILON
'''
Given three points a,b,c,
returns True if and only if 
a,b,c represents a counter-clockwise sequence
(subject to floating-point precision)
'''
def ccw(a, b, c):
	return triangleArea(a,b,c) > EPSILON

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

'''
Find the left most point in the graph
'''
def mostLeft(graph):
    left = 0
    for point in range(1, len(graph)):
        if graph[point][0] < graph[left][0]:
            left = point
        elif graph[point][0] == graph[left][0]:
            if graph[point][1] > graph[left][1]:
                left = point
        
    return left

'''
Implementation of the Jarvis algorithm to find
and form any polygons under 6 points
'''
def wrap(graph):
    '''
    Convex Hull algorithm used to find the convex
    shape enclosure of a graph
    '''
    if len(graph) < 3:
        return None

    left = mostLeft(graph)

    convex_hull = []

    pointer = left

    while(True):

        convex_hull.append(pointer)

        clockwise = (pointer + 1) % len(graph)

        for point in range(len(graph)):
            if ccw(graph[pointer], graph[point], graph[clockwise]):
                clockwise = point

        pointer = clockwise

        if(pointer == left):
            break
    
    hull = []
    for point in convex_hull:
        hull.append(graph[point])

    return hull

'''
Merge the polygons
'''
def merge(left, right):
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

        while ccw(left[upperLeft], right[upperRight], right[(p2 + upperRight - 1) % p2]) or ccw(left[upperLeft], right[upperRight], right[(p2 + upperRight - 1) % p2]):
            upperRight = (p2 + upperRight - 1) % p2
            flag = False
    
    # Let's find the lower tanget
    lowerLeft = l
    lowerRight = r
    flag = False
    while flag == False:
        flag = True
        while cw(left[lowerLeft], right[lowerRight], right[(lowerRight + 1) % p2]) or collinear(left[lowerLeft], right[lowerRight], right[(lowerRight + 1) % p2]) :
            lowerRight = (lowerRight + 1) % p2

        while ccw(right[lowerRight], left[lowerLeft], left[(p1 + lowerLeft - 1) % p1]) or collinear(right[lowerRight], left[lowerLeft], left[(p1 + lowerLeft - 1) % p1]) :
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

def divide(graph):
    p = len(graph)
    if p < 6:
        return wrap(graph)

    left = []
    right = []

    for point in range(0, int(p/2)):
        left.append(graph[point])

    for point in range(int(p/2), p):
        right.append(graph[point])

    left_polygon = divide(left)
    right_polygon = divide(right)

    return merge(left_polygon, right_polygon)

'''
Removes duplicates from a list and represents a list as a set
'''
def listToSet(l):
    i = 0
    while i < len(l) - 1:
        if l[i][0] == l[i + 1][0]:
            if l[i][1] == l[i + 1][1]:  
                del l[i]
            else:
                i += 1
        else:
            i += 1
    return l

'''
Replace the implementation of computeHull with a correct computation of the convex hull
using the divide-and-conquer algorithm
'''
def computeHull(graph):
    sorted_graph = sorted(graph, key = lambda point: point[0])
    graph_set = listToSet(sorted_graph)
    return divide(graph_set)