from src.helper import *
from src.neuralnet import *
from src.sensor import Sensor


class Robot:
    def __init__(self, WIDTH, HEIGHT, walls, weights=None, SCALE=40, use_nn=False, is_odometry_based=False):
        self.x = 100
        self.y = 150
        self.theta = 0
        self.radius = 30
        self.wheel_dist = self.radius * 2  # Distance between wheels
        self.is_odometry_based = is_odometry_based
        self.kinematical_parameters = [0, 0]  # left - [0], right - [1]

        if is_odometry_based:
            self.kinematical_parameter_names = ['left wheel', 'right wheel']
        else:
            self.kinematical_parameter_names = ['translational velocity', 'angular velocity']

        self.check_if_rotates()
        self.width = WIDTH
        self.height = HEIGHT
        self.walls = walls
        self.scale = SCALE
        self.vertical_bins = np.linspace(0, HEIGHT, num=SCALE)
        self.horizontal_bins = np.linspace(0, WIDTH, num=SCALE)
        self.visited = np.zeros((SCALE, SCALE))
        self.visited_arr = []
        self.old_x_bin, self.old_y_bin = np.digitize(self.x, self.horizontal_bins), np.digitize(self.y,
                                                                                                self.vertical_bins)
        self.prev_x = self.x
        self.prev_y = self.y
        self.prev_theta = self.theta
        self.use_nn = use_nn

        self.range_beacon_sensor = 200

        # Fitness stats
        self.fitness = 0
        self.n_not_moved = 0
        self.n_collisions = 0
        self.n_visited_bins = 0

        self.nn = RNN(inputs=12, outputs=2, hidden_layer_size=6, weights=weights)

        self.sensors = []
        num_sensors = 12
        for i in range(num_sensors):
            self.sensors.append(Sensor(i * (2 * math.pi / num_sensors)))

    def set_odometry_based_model(self):
        self.is_odometry_based = True
        self.kinematical_parameter_names = ['left wheel', 'right wheel']

    def set_pos(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta

    def get_pos(self):
        return int(self.x), int(self.y)

    def check_sensors(self, collision=False):
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
                moveback = point_from_angle(self.x, self.y, sensor_bearing, -(self.radius - sensor.value))
                self.x = moveback[0]
                self.y = moveback[1]

                collision = self.check_sensors(True)
                break

        return collision

    def check_beacons(self, beacons):
        """
        Iterate over all the beacons and checks if they are in the range of the beacon sensor
        :return: list of beacons found by the robot
        """
        saw_beacons = []
        for beacon in beacons:
            if distance(beacon, [self.x, self.y]) < self.range_beacon_sensor:
                saw_beacons.append(beacon)

        return saw_beacons

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
        return (self.kinematical_parameters[1] + self.kinematical_parameters[0]) / 2

    def calculate_R(self):
        """
        Calculate distance from midpoint to ICC basing on the wheel speed and width
        :return:
        """
        return (self.wheel_dist / 2) * (self.kinematical_parameters[0] + self.kinematical_parameters[1]) / (
                self.kinematical_parameters[1] - self.kinematical_parameters[0])

    def calculate_rate_of_rotation(self):
        """
        Calculate rate of rotation basing on speed of the wheels
        :return:
        """
        return (self.kinematical_parameters[1] - self.kinematical_parameters[0]) / self.wheel_dist

    def get_ICC_coordinates(self):
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
        if math.isclose(self.kinematical_parameters[0], self.kinematical_parameters[1]):
            self.is_rotating = False
        else:
            self.is_rotating = True

    def update_position(self):
        if self.is_odometry_based:
            self.update_position_odometry_based()
        else:
            self.update_position_velocity_based()

    def update_position_velocity_based(self):
        """
        Update position and angle of the robot basing on velocity model.
        """
        increment_matrix = np.array([[math.cos(self.theta), 0],
                                     [math.sin(self.theta), 0],
                                     [0, 1]])

        [self.x, self.y, self.theta] = [self.x, self.y, self.theta] + np.dot(increment_matrix,
                                                                             self.kinematical_parameters)
        self.introduce_noise_kinematics()
        self.check_periodicity()
        self.update_fitness()

    def introduce_noise_kinematics(self):
        if np.random.random() < 0.01:
            if self.is_odometry_based \
                    and (abs(self.kinematical_parameters[0]) > 0.01
                         or abs(self.kinematical_parameters[1]) > 0.01):
                self.kinematical_parameters[0] += (np.random.random() - 0.5) * 0.01
            elif not self.is_odometry_based:
                self.kinematical_parameters[0] += (np.random.random() - 0.5) * 0.001

        if np.random.random() < 0.01:
            if self.is_odometry_based \
                    and (abs(self.kinematical_parameters[0]) > 0.01
                         or abs(self.kinematical_parameters[1]) > 0.01):
                self.kinematical_parameters[1] += (np.random.random() - 0.5) * 0.01
            elif not self.is_odometry_based and abs(self.kinematical_parameters[0]) > 0.01:
                self.kinematical_parameters[1] += (np.random.random() - 0.5) * 0.0001

    def update_position_odometry_based(self):
        """
        Updating position and angle of the robot. Firstly check if the rotation is present, then
        apply corresponding formula.
        """

        # Shape feedback of sensors (distance measure should not be linear)
        # Closer to wall = exponentially higher sensor value
        # Far away from wall = 0 + 1 (we add 1 to prevent 0 multiplication when there is no wall in sight)
        def shape(x):
            exp = 2
            return ((Sensor.MAX_SENSOR_VALUE - x) ** exp) + 1

        sensor_values = [shape(sensor.value) for sensor in self.sensors]

        # Propagate ANN
        if self.use_nn:
            outputs = self.nn.propagate(sensor_values) * 5
            self.kinematical_parameters = outputs

        self.introduce_noise_kinematics()
        # Update position
        self.check_if_rotates()
        if self.is_rotating:
            omega = self.calculate_rate_of_rotation()
            ICC_x, ICC_y = self.get_ICC_coordinates()

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
            self.check_periodicity()
        else:
            self.x += self.kinematical_parameters[0] * math.cos(self.theta)
            self.y += self.kinematical_parameters[0] * math.sin(self.theta)

        self.update_fitness()

    def check_periodicity(self):
        # Reset degrees after 2 PI radians
        if self.theta >= 2 * math.pi:
            self.theta = self.theta - 2 * math.pi
        elif self.theta <= -2 * math.pi:
            self.theta = self.theta + 2 * math.pi

    def set_NN(self, NN):
        self.nn = NN

    def get_NN_weights_flatten(self):
        return self.nn.flatten()

    def get_NN_weights(self):
        return self.nn.weights

    def update_fitness(self):
        collided = self.check_sensors()
        x, y = int(round(self.x)), int(round(self.y))
        position = [x, y]

        x_bin_idx = np.digitize(x, self.horizontal_bins)
        y_bin_idx = np.digitize(y, self.vertical_bins)

        # Increase fitness calculated when new space visited
        if self.visited[x_bin_idx, y_bin_idx] == 0:
            self.visited[x_bin_idx, y_bin_idx] = 1
            self.n_visited_bins += 1

        if position not in self.visited_arr:
            self.visited_arr.append([x, y])

        # Decrease fitness if wall collided
        if collided:
            self.n_collisions += 1

        # Decrease fitness if didnt move in discrete space:
        # if self.old_x_bin == x_bin_idx and self.old_y_bin == y_bin_idx:
        # 	delta_fitness -= 1

        # Count the number of updates the robot has not moved
        # if self.prev_x == self.x and self.prev_y == self.y and self.prev_theta == self.theta:
        if round(self.prev_x) == round(self.x) and round(self.prev_y) == round(self.y):
            self.n_not_moved += 1
        else:
            self.n_not_moved = 0

        self.fitness = self.cost_function()

        # Save old bin and real pos
        self.old_x_bin, self.old_y_bin = x, y
        self.prev_x = self.x
        self.prev_y = self.y
        self.prev_theta = self.theta

    def cost_function(self):
        """Cost functions"""
        f = 2

        # Function 1: only covered distance
        if f == 1:
            return self.n_visited_bins

        # Function 2: covered distance minus log(collisions)
        if f == 2:
            return self.n_visited_bins - math.log(self.n_collisions + 1) * 10

    def set_walls(self, walls):
        self.walls = walls
