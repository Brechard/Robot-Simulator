import math
import numpy as np
import numpy.linalg as la


def point_from_angle(x, y, angle, length):
    """return the endpoint of a line starting in x,y using the given angle and length"""
    x = x + length * math.cos(angle)
    y = y + length * math.sin(angle)
    return x, y


def distance(point_1, point_2):
    """Distance between the 2 points"""
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)


def get_line_angle(point_1, point_2):
    """Returns the angle of a line that goes from point_1 to point_2"""
    return ((math.atan2((point_1[1] - point_2[1]), (point_1[0] - point_2[0])) * 180.0 / math.pi) + 360) % 360


def py_ang(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'    """
    cosang = np.dot(v1, v2)
    sinang = la.norm(np.cross(v1, v2))
    return np.arctan2(sinang, cosang)
