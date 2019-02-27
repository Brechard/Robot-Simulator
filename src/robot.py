import math
from src.neuralnet import *
import numpy as np

from src.helper import *
from src.sensor import Sensor


class Robot():
    def __init__(self, WIDTH, HEIGHT, walls, weights = None):
        self.x = 100
        self.y = 200
        self.theta = 0
        self.radius = 30
        self.wheel_dist = self.radius * 2  # Distance between wheels
        self.speed = [0, 0]  # left - [0], right - [1]
        self.is_rotating = self.check_if_rotates()
        self.width = WIDTH
        self.height = HEIGHT
        self.walls = walls

        self.nn = RNN(inputs=12, outputs=2, hidden_layer_size=5, weights=weights)

        self.sensors = []
        num_sensors = 12
        for i in range(num_sensors):
            self.sensors.append(Sensor(i * (2 * math.pi / num_sensors)))
        self.check_sensors()

    def get_pos(self):
        return int(self.x), int(self.y)

    def check_sensors(self):
        collision = False
        for sensor in self.sensors:
            sensor_bearing = (sensor.angle + self.theta) % (2 * math.pi)  # Sensor angle is relative to the robot
            sensor.value = sensor.MAX_SENSOR_VALUE
            sensor.p2 = point_from_angle(self.x, self.y, sensor_bearing, sensor.value)
            for wall in self.walls:
                crossover = wall.intersectsLine((self.x, self.y), sensor.p2)
                if crossover != False:
                    dist = distance((self.x, self.y), crossover)
                    sensor.value = dist
                    sensor.p2 = crossover

            # Check for wall collisions
            if self.radius > sensor.value + 0.0005:
                collision = True
                moveback = point_from_angle(self.x, self.y, sensor_bearing, -(self.radius - sensor.value))
                self.x = moveback[0]
                self.y = moveback[1]

                self.check_sensors()
                break

        return collision

    def get_sensor_values(self):
        list = []
        for sensor in self.sensors:
            list.append(sensor.value)
        return list

    def calculate_speed(self):
        """
        Calculate the speed of the robot basing on the wheel speed
        :return: Velocity of the robot
        """
        return (self.speed[1] + self.speed[0]) / 2

    def calculate_R(self):
        """
        Calculate distance from midpoint to ICC basing on the wheel speed and width
        :return:
        """
        return (self.wheel_dist / 2) * (self.speed[0] + self.speed[1]) / (self.speed[1] - self.speed[0])

    def calculate_rate_of_rotation(self):
        """
        Calculate rate of rotation basing on speed of the wheels
        :return:
        """
        return (self.speed[1] - self.speed[0]) / self.wheel_dist

    def get_ICC_coordinates(self, R):
        """
        Calculate the coordinates of ICC
        :param R: Distance from midpoint to ICC
        :return: Coordinates of the ICC
        """
        R = self.calculate_R()
        return (self.x - R * math.sin(self.theta)), (self.y + R * math.cos(self.theta))

    def check_if_rotates(self):
        """
        Checks if the velocities of the wheels are equal and returns corresponding True/False value
        :return:
        """
        if math.isclose(self.speed[0], self.speed[1]):
            self.is_rotating = False
        else:
            self.is_rotating = True

    def update_position(self):
        """
        Updating position and angle of the robot. Firstly check if the rotation is present, then
        apply corresponding formula.
        """

        # TODO implement genetic algorithm
        outputs = self.nn.propagate([sensor.value for sensor in self.sensors])
        self.speed = outputs

        self.check_if_rotates()

        if self.is_rotating:
            omega = self.calculate_rate_of_rotation()
            R = self.calculate_R()
            ICC_x, ICC_y = self.get_ICC_coordinates(R)

            # Calculation of the position and angle with the forward kinematics
            rotation_matrix = np.array([[math.cos(omega), -math.sin(omega), 0],
                                        [math.sin(omega), math.cos(omega), 0],
                                        [0, 0, 1]])
            coordinate_vector = np.array([self.x - ICC_x, self.y - ICC_y, 0])
            rotation_origin_vector = np.array([ICC_x, ICC_y, omega])

            result = np.dot(rotation_matrix, coordinate_vector) + rotation_origin_vector
            self.x = result[0]
            self.y = result[1]
            self.theta -= result[2]
            # print(R)
            # Reset degrees after 2 PI radians
            if self.theta >= 2 * math.pi:
                self.theta = self.theta - 2 * math.pi
            elif self.theta <= -2 * math.pi:
                self.theta = self.theta + 2 * math.pi
        else:
            self.x += self.speed[0] * math.cos(self.theta)
            self.y += self.speed[0] * math.sin(self.theta)

        return self.check_sensors(), int(round(self.x)), int(round(self.y))

    def set_NN(self, NN):
        self.nn = NN

    def get_NN_weights_flatten(self):
        return self.nn.flatten()

    def get_NN_weights(self):
        return self.nn.weights
