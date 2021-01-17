#written by gyosh


import numpy as np
import math
import sys

def eq(a, b):
    return abs(a - b) < sys.float_info.epsilon

def lt(a, b):
    return (a < b) and not eq(a, b)

def lteq(a,b):
    return (a<b) or eq(a,b)

def between(a,b,c): #c is between a and b
    return (lteq(a,c) and lteq(c,b)) or (lteq(b,c) and lteq(c,a))

def intersect(x1, y1, a1, x2, y2, a2):
    a1 = math.radians(a1)
    a2 = math.radians(a2)

    u = np.array([math.cos(a1), math.sin(a1)])
    v = np.array([math.cos(a2), math.sin(a2)])
    b = np.array([x1 - x2, y1 - y2])
    A = np.array([
        [-u[0], v[0]],
        [-u[1], v[1]]
    ])

    if eq(np.linalg.det(A), 0):
        # No solution or infinitely many solutions
        return None

    # We know A*x = b, so x = Ainv*b
    x = np.linalg.inv(A).dot(b)

    if any(lt(k, 0) for k in x):
        # If any of the elements in x is < 0, then the
        # the ray needs to travel backwards in order to intersect
        return None

    # Recover the intersection point
    k = x[0]
    intersection = np.array([x1, y1]) + k*u
    return intersection

'''
#examples
# Converge
print(intersect(0, 0, 45, 1, 0, 135))

# T
print(intersect(0, 0, 90, 1, 0, 180))

# Diverge
print(intersect(0, 0, 135, 1, 0, 45))

# Overlap
print(intersect(0, 0, 0, 1, 0, 180))
print(intersect(1, 1, 45, 0, 0, 225))

# Parallel
print(intersect(0, 0, 90, 1, 0, 90))
'''


'''import math
import numpy

def intersect(x1,y1,a1,x2,y2,a2):
    #angles need to be in degrees
    l3 = ((x1-x2)**2+(y1-y2)**2)**0.5
    #l3 is the distance between points 1 and 2
    try:
        a3 = 180+math.degrees(math.atan((y2-y1)/(x2-x1)))-a2
        #a3 is the angle between point 1, point 2, and intersection
    except:
        a3 = 270-a2 #in case x2 == x1, the tan will be 90
    l1 = l3*math.sin(math.radians(a3))/math.sin(math.radians(a2-a1))
    #l1 is the distance from point 1 to the intersection. Use law of sines
    xint = l1*math.cos(math.radians(a1))+x1
    yint = l1*math.sin(math.radians(a1))+y1
    return (xint,yint)
#figure out if the angle between intersection, 2, and horizontal is a2 or 360-a2

def equal(a,b):
    return abs(a-b) < 0.0000001

def intersect(x1, y1, a1, x2, y2, a2):
    a1 = math.radians(a1)
    a2 = math.radians(a2)
    matrix1 = numpy.array([[x1-x2,
               y1-y2]])
    print(matrix1)
    matrix2 = numpy.array([[-math.cos(a1),math.cos(a2)],
               [-math.sin(a1),math.sin(a2)]])
    print(matrix2)
    matrix2i = numpy.array([[math.sin(a2),-math.cos(a2)],[math.sin(a1),-math.cos(a1)]])/(math.sin(a2)*-1*math.cos(a1)-math.cos(a2)*-1*math.sin(a1))
    k1k2 = numpy.multiply(matrix2i,matrix1)
    print(k1k2)
    k1 = k1k2[0][0]
    k2 = k1k2[1][1]
    print(k1,k2)
    intersection = (x1+k1*math.cos(a1),y1+k1*math.sin(a1))
    print((x2+k2*math.cos(a2),y2+k2*math.sin(a2)))
    return intersection
    print(matrix1)
    print(matrix2)
    print(numpy.divide(matrix1,matrix2))
    return (numpy.divide(matrix1,matrix2)[0][0],
            numpy.divide(matrix1,matrix2)[0][1])'''

