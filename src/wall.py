import numpy as np
from helper import *


class Wall():
    """ Wall the player can run into. """

    def __init__(self, p1, p2):
        """ Constructor for the wall that the player can run into. """
        self.p1 = p1
        self.p2 = p2
        self.angle = get_line_angle(p1, p2)

    def intersectsLine(self, line2_p1, line2_p2):
        """ If the given line intersects the wall, returns the position of this intersection """

        # Check if a line intersection is possible within range
        if ((self.p1[0] > line2_p1[0] and self.p1[0] > line2_p2[0] and self.p2[0] > line2_p1[0] and self.p2[0] >
             line2_p2[0]) or
                (self.p1[0] < line2_p1[0] and self.p1[0] < line2_p2[0] and self.p2[0] < line2_p1[0] and self.p2[0] <
                 line2_p2[0]) or
                (self.p1[1] > line2_p1[1] and self.p1[1] > line2_p2[1] and self.p2[1] > line2_p1[1] and self.p2[1] >
                 line2_p2[1]) or
                (self.p1[1] < line2_p1[1] and self.p1[1] < line2_p2[1] and self.p2[1] < line2_p1[1] and self.p2[1] <
                 line2_p2[1])):
            return False

        # Get axis differences
        diffX = (self.p1[0] - self.p2[0], line2_p1[0] - line2_p2[0])
        diffY = (self.p1[1] - self.p2[1], line2_p1[1] - line2_p2[1])

        # Get intersection
        d = np.linalg.det([diffX, diffY])
        if d == 0:
            return False
        det = (np.linalg.det([self.p1, self.p2]), np.linalg.det([line2_p1, line2_p2]))
        x = np.linalg.det([det, diffX]) / d
        y = np.linalg.det([det, diffY]) / d

        # Check if it is within range
        margin = 0.0001
        if (x < min(self.p1[0], self.p2[0]) - margin or
                x > max(self.p1[0], self.p2[0]) + margin or
                y < min(self.p1[1], self.p2[1]) - margin or
                y > max(self.p1[1], self.p2[1]) + margin or
                x < min(line2_p1[0], line2_p2[0]) - margin or
                x > max(line2_p1[0], line2_p2[0]) + margin or
                y < min(line2_p1[1], line2_p2[1]) - margin or
                y > max(line2_p1[1], line2_p2[1]) + margin):
            return False

        return x, y
