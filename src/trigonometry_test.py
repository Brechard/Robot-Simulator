import unittest
import trigonometry
import math


class TrigonometryTest(unittest.TestCase):

    def round_values(self, points):
        return [round(point, 3) for point in points]

    def test_calculate_position(self):
        # test_beacon_position = ((0, 0), (10, 0), (0, 10))
        # angles = (math.pi, math.pi / 2, 3 * math.pi / 2)
        #
        # self.assertEqual([5.0, 5.0], self.round_values(trigonometry.calculate_position(angles, test_beacon_position)))
        # trigonometry.plot_and_calculate_position(angles, test_beacon_position)

        test_beacon_position = ((0, 10), (0, 0), (10, 0))
        # angles = (0, math.pi / 4, math.pi / 2)
        distances = [10, 15, 10]
        import numpy as np
        print(trigonometry.gps_solve(distances, np.array(test_beacon_position)))
        x = []
        y = []
        for point in test_beacon_position:
            x.append(point[0])
            y.append(point[1])
        import matplotlib.pyplot as plt
        plt.scatter(x, y)
        x, y = trigonometry.gps_solve(distances, np.array(test_beacon_position))
        plt.scatter(x, y)
        plt.show()

        # self.assertEqual([10.0, 10.0], self.round_values(trigonometry.calculate_position(angles, test_beacon_position)))
        trigonometry.plot_and_calculate_position(angles, test_beacon_position)