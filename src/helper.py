import math


def point_from_angle(x, y, angle, length):
    """return the endpoint of a line starting in x,y using the given angle and length"""
    x = x + length * math.cos(angle)
    y = y + length * math.sin(angle)
    return x, y


def distance(point_1, point_2):
    """Distance between the 2 points"""
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)


def round_angle(angle, base = 90):
    return int(base * round(float(angle) / base))


def get_line_midpoint(point_1, point_2):
    """Returns the halfway point inbetween point_1 and point_2"""
    return ((point_1[0] + point_2[0]) / 2), ((point_1[1] + point_2[1]) / 2)


def get_line_angle(point_1, point_2):
    """Returns the angle of a line that goes from point_1 to point_2"""
    return ((math.atan2((point_1[1]-point_2[1]), (point_1[0]-point_2[0])) * 180.0/math.pi) + 360) % 360