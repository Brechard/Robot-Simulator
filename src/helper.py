import math


def point_from_angle(x, y, angle, length):
    """return the endpoint of a line starting in x,y using the given angle and length"""
    x = x + length * math.cos(angle)
    y = y + length * math.sin(angle)
    return x, y


def distance(point_1, point_2):
    """Distance between the 2 points"""
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)
