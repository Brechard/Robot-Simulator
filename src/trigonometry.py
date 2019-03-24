import numpy as np
import math
import matplotlib.pyplot as plt

COT_MAX = 100000000

test_beacon_position = ((0, 0), (10, 0), (0, 10))
angles = (math.pi, math.pi/2,  3*math.pi/2)


def check_boundaries(max_value, *args):
    result = []
    for value in args:
        if value > max_value:
            value = max_value
        elif value < - max_value:
            value = -max_value

        result.append(value)
    return result

def calculate_position(angles, positions):
    
    cot_12 = 1 / math.tan(angles[1] - angles[0])
    cot_23 = 1 / math.tan(angles[2] - angles[1])
    cot_31 = (1.0 - cot_12 * cot_23) / (cot_12 + cot_23)

    cot_12, cot_23, cot_31 = check_boundaries(COT_MAX, cot_12, cot_23, cot_31)

    x1_ = positions[0][0] - positions[1][0]
    y1_ = positions[0][1] - positions[1][1]
    x3_ = positions[2][0] - positions[1][0]
    y3_ = positions[2][1] - positions[1][1]

    c12x = x1_ + cot_12 * y1_
    c12y = y1_ - cot_12 * x1_

    c23x = x3_ - cot_23 * y3_
    c23y = y3_ + cot_23 * x3_

    c31x = (x3_ + x1_) + cot_31 * (y3_ - y1_)
    c31y = (y3_ + y1_) - cot_31 * (x3_ - x1_)

    k31 = (x3_ * x1_) + (y3_ * y1_) + cot_31 * ((y3_ * x1_) - (x3_ * y1_))

    D = (c12x - c23x) * (c23y - c31y) - (c23x - c31x) * (c12y - c23y)
    invD = 1.0 / D

    K = k31 * invD

    X = K * (c12y - c23y) + positions[1][0]
    Y = K * (c23x - c12x) + positions[1][1]

    Q = abs(invD)

    return X, Y

print(calculate_position(angles, test_beacon_position))
x = []
y = []
for point in test_beacon_position:
    x.append(point[0])
    y.append(point[1])
plt.scatter(x, y)
x, y = calculate_position(angles, test_beacon_position)
plt.scatter(x, y)
plt.show()


