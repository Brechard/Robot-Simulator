import sys
from datetime import datetime

import pygame
from pygame.locals import *
import numpy as np

from algorithms.neuralnet import *
from src.helper import *
from src.model.robot import Robot
from src.model.wall import Wall
import time
import helper
from algorithms.experiments import Experiments

WIDTH = 840
HEIGHT = 600
# WIDTH = 500
# HEIGHT = 350

# some colors
black = (0, 0, 0)
dust = (128, 128, 128)
blue = (20, 80, 155)
red = (255, 0, 0)
green = (11, 102, 35)
yellow = (230, 230, 52)
orange = (255, 110, 20)
green_sensor = (53, 98, 68)
stats_height = 100
pygame.font.init()
font = pygame.font.SysFont('arial', 20)

# parameters
button_step = 5


class GFX:
    wall_list = []
    robot_size = 60

    def __init__(self, weights=None, wall_list=None):

        # Outer walls
        self.padding = 20
        if wall_list:
            self.wall_list = wall_list
        else:
            self.wall_list.append(Wall((self.padding, self.padding), (WIDTH - self.padding, self.padding)))
            self.wall_list.append(
                Wall((self.padding, HEIGHT - self.padding), (WIDTH - self.padding, HEIGHT - self.padding)))
            self.wall_list.append(Wall((self.padding, self.padding), (self.padding, HEIGHT - self.padding)))
            self.wall_list.append(
                Wall((WIDTH - self.padding, self.padding), (WIDTH - self.padding, HEIGHT - self.padding)))

        # self.build_walls()

        self.visited = np.zeros((WIDTH, HEIGHT))
        self.visited_arr = []

        # Init pygame window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + stats_height), pygame.HWSURFACE | pygame.DOUBLEBUF)

        # init pygame window for mac users
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        pygame.display.set_caption("ARS")

        # Init robot
        self.robot = Robot(WIDTH, HEIGHT, self.wall_list, weights)
        self.add_beacons()
        self.stop = False
        self.experiments = Experiments()

    def add_beacons(self, n_random_beacons=10):
        beacons = []
        beacon_step = 200
        for i in range(int(WIDTH / beacon_step) + 1):
            for j in range(int(HEIGHT / beacon_step) + 1):
                x = 20 + int(np.random.normal(i * beacon_step, 20))
                y = 20 + int(np.random.normal(j * beacon_step, 20))
                if x < 20: x = 20
                if x > WIDTH - 20: x = WIDTH - 20
                if y < 20: y = 20
                if y > HEIGHT - 20: y = HEIGHT - 20
                beacons.append((x, y))
                # print("Beacon appended", beacons[-1])

        self.robot.beacons = beacons

    def build_walls(self):
        self.padding = 230
        self.wall_list.append(Wall((self.padding, self.padding), (WIDTH - self.padding, self.padding)))
        self.wall_list.append(
            Wall((self.padding, HEIGHT - self.padding), (WIDTH - self.padding, HEIGHT - self.padding)))
        self.wall_list.append(Wall((self.padding, self.padding), (self.padding, HEIGHT - self.padding)))
        self.wall_list.append(Wall((WIDTH - self.padding, self.padding), (WIDTH - self.padding, HEIGHT - self.padding)))
        self.wall_list.append(Wall((self.padding * 2, self.padding), (WIDTH - self.padding, self.padding)))
        self.wall_list.append(
            Wall((self.padding, HEIGHT - self.padding), (WIDTH - self.padding, HEIGHT - self.padding)))
        self.wall_list.append(Wall((self.padding * 2, self.padding), (self.padding, HEIGHT - self.padding)))
        self.wall_list.append(Wall((WIDTH - self.padding, self.padding), (WIDTH - self.padding, HEIGHT - self.padding)))

    def set_nn_controller(self):
        self.robot.use_nn = True

    def set_odometry_based_model(self):
        self.robot.set_odometry_based_model()

    def load_image(self, filename, transparent=False):
        try:
            image = pygame.image.load(filename).convert()
        except pygame.error as message:
            raise SystemExit(message)
        if transparent:
            color = image.get_at((0, 0))
            image.set_colorkey(color)
        return image

    def main(self, draw, kill_when_stuck=False, max_time=100, use_steps=True):
        clock = pygame.time.Clock()
        # background = load_image("../images/background.png")
        if not draw:
            pygame.display.iconify()

        self.start_time = datetime.now()
        self.last_time = datetime.now()

        for i in range(max_time):
            while self.stop:
                # Handle inputs
                for events in pygame.event.get():
                    self.stop_event(events)
                continue

            # Handle inputs
            for events in pygame.event.get():
                self.event(events)

            # Update state
            self.update()

            # Kill simulation if robot is stuck (if robot is not moving, the next input for the ANN will be the same
            # as the previous input. because the environment is static we can conclude that the robot is not going to
            # move again in any future state)
            if kill_when_stuck and self.robot.n_not_moved > 50:
                self.robot.fitness = -100
                break

            # Draw current state
            if draw:
                self.draw(i)

            obs_pos = np.array(
                [self.robot.observed_position[0], self.robot.observed_position[1], self.robot.observed_orientation])
            self.experiments.store_values(real_pos=self.robot.get_state(),
                                          obs_pos=obs_pos,
                                          pred_pos=self.robot.predictions[-1],
                                          kalman_pos=self.robot.believe_states[-1])
            if use_steps:
                time.sleep(0.1)

    def event(self, events):
        if events.type == QUIT:
            sys.exit(0)
        elif events.type == KEYUP:
            if events.key == K_w:
                self.robot.kinematical_parameters[
                    0] += button_step  # Left wheel increment / Increment translational velocity
            elif events.key == K_s:
                self.robot.kinematical_parameters[
                    0] -= button_step  # Left wheel decrement / Decrement translational velocity
            elif events.key == K_o:
                self.robot.kinematical_parameters[1] += button_step  # Right wheel increment
            elif events.key == K_l:
                self.robot.kinematical_parameters[1] -= button_step  # Right wheel decrement
            elif events.key == K_x:
                self.robot.kinematical_parameters = [0, 0]  # Set to 0
            elif events.key == K_t:
                self.robot.kinematical_parameters[0] += button_step  # Both increment
                self.robot.kinematical_parameters[1] += button_step  # Both increment
            elif events.key == K_g:
                self.robot.kinematical_parameters[0] -= button_step  # Both decrement
                self.robot.kinematical_parameters[1] -= button_step  # Both decrement
            elif events.key == K_a:
                self.robot.kinematical_parameters[1] -= button_step / 50  # Decrement angular velocity
            elif events.key == K_d:
                self.robot.kinematical_parameters[1] += button_step / 50  # Increment angular velocity
            elif events.key == K_p:
                self.stop = True

    def stop_event(self, events):
        if events.type == KEYUP and events.key == K_p:
            self.stop = False

    def update(self):
        """
        Update the positions of the robot and return the value to add to the fitness function.
        When there is a collision with a wall we give -5 points and when we visit a new position we add 1 point.
        :return: value to add to the fitness function
        """
        # Update robot step
        now = datetime.now()
        time_diff = now - self.last_time
        time_diff = time_diff.total_seconds()
        self.last_time = now

        self.robot.update_position()
        self.visited_arr = self.robot.visited_arr

    def draw(self, update):

        # Reset screen
        self.screen.fill([255, 255, 255])

        # Dust
        if len(self.visited_arr) > 1:
            for pos in range(1, len(self.visited_arr)):
                pygame.draw.line(self.screen, black, self.visited_arr[pos - 1], self.visited_arr[pos], 2)

        # Draw walls
        for wall in self.wall_list:
            pygame.draw.line(self.screen, black, wall.p1, wall.p2)

        beacons, _, _ = self.robot.check_beacons()
        for beacon in beacons:
            pygame.draw.circle(self.screen, black, beacon[:2], 10, 0)
            pygame.draw.line(self.screen, green, (self.robot.x, self.robot.y), beacon[:2], 2)

        # Draw circle for the omnidirectional beacon sensor
        pygame.draw.circle(self.screen, green_sensor, self.robot.get_pos(), self.robot.range_beacon_sensor, 1)

        # Sensors
        for i, sensor in enumerate(self.robot.sensors):
            pygame.draw.line(self.screen, red, self.robot.get_pos(), sensor.p2)
            if sensor.value < sensor.MAX_SENSOR_VALUE:
                text_surface = font.render(str(i) + ": " + "{0:.0f}".format(sensor.value), False, red)
                self.screen.blit(text_surface, sensor.p2)

        # Robot
        pygame.draw.circle(self.screen, blue, self.robot.get_pos(), self.robot.radius, 0)
        pygame.draw.line(self.screen, black, (self.robot.x, self.robot.y),
                         point_from_angle(self.robot.x, self.robot.y, self.robot.theta, self.robot.radius), 2)

        self.draw_kinematics(update)
        self.draw_positions()
        self.draw_performance()
        self.draw_prediction()
        self.draw_estimated()
        self.draw_observed()

        # x, y, width, height = self.robot.believe_states[-1][0], self.robot.believe_states[-1][1], \
        #                       self.robot.covariance[0][0], self.robot.covariance[1][1]
        # print(x, y, x + width, y + height)
        # pygame.draw.ellipse(self.screen, black, [x, y, x + width, y + height], 1)

        # pygame.draw.ellipse(self.screen, red, [500, 500, 100, 50], 1)
        # pygame.draw.ellipse(self.screen, green, [500, 500, 2, 2], 1)
        # pygame.draw.circle(self.screen, blue, [500, 500], 2, 0)

        # self.draw_elipses()

        pygame.display.update()

    def draw_elipses(self):
        x, y = self.robot.believe_states[-1][:2]
        # x, y = self.robot.x, self.robot.y
        # width, height = 2 * x * 10, 2 * y * 10
        width, height = 100, 200

        surface = pygame.Surface((width, height))
        size = (0, 0, width, height)

        # drawing an ellipse onto the
        pygame.draw.ellipse(surface, red, size)
        left_up_corner = [int(x - width / 2), int(y - height / 2)]
        print("left up corner", left_up_corner)

        self.screen.blit(surface, left_up_corner)
        pygame.draw.circle(self.screen, blue, left_up_corner, 10, 0)
        pygame.draw.circle(self.screen, blue, [int(x), int(y)], 10, 0)

    def draw_observed(self):
        center_point = [int(x) for x in self.robot.observed_position[:2]]
        end_point = helper.get_point_from_angle(center_point, self.robot.observed_orientation, 15)
        pygame.draw.circle(self.screen, green, center_point, 16, 5)
        pygame.draw.line(self.screen, green, center_point, end_point, 5)

        text_surface = font.render("observed", False, red)
        self.screen.blit(text_surface, (630, stats_height + HEIGHT - 60))

        pygame.draw.circle(self.screen, green, (608, stats_height + HEIGHT - 47), 10, 4)
        pygame.draw.line(self.screen, green, (608, stats_height + HEIGHT - 47), (616, stats_height + HEIGHT - 47), 4)

    def draw_prediction(self):
        center_point = [int(x) for x in self.robot.predictions[-1][:2]]
        end_point = helper.get_point_from_angle(center_point, self.robot.predictions[-1][2], 15)
        pygame.draw.circle(self.screen, orange, center_point, 16, 5)
        pygame.draw.line(self.screen, orange, center_point, end_point, 5)

        text_surface = font.render("estimated", False, red)
        self.screen.blit(text_surface, (630, stats_height + HEIGHT - 100))
        pygame.draw.circle(self.screen, orange, (608, stats_height + HEIGHT - 87), 10, 4)
        pygame.draw.line(self.screen, orange, (608, stats_height + HEIGHT - 87), (616, stats_height + HEIGHT - 87), 4)

    def draw_estimated(self):
        # pygame.draw.circle(self.screen, dust, [int(x) for x in self.robot.believe_states[-1][:2]], 15, 5)
        center_point = [int(x) for x in self.robot.believe_states[-1][:2]]
        end_point = helper.get_point_from_angle(center_point, self.robot.believe_states[-1][2], 15)
        pygame.draw.circle(self.screen, dust, center_point, 16, 5)
        pygame.draw.line(self.screen, dust, center_point, end_point, 5)

        text_surface = font.render("corrected", False, red)
        self.screen.blit(text_surface, (630, stats_height + HEIGHT - 80))
        pygame.draw.circle(self.screen, dust, (608, stats_height + HEIGHT - 67), 10, 4)
        pygame.draw.line(self.screen, dust, (608, stats_height + HEIGHT - 67), (616, stats_height + HEIGHT - 67), 4)

    def draw_kinematics(self, update):
        # Wheel speeds
        text_surface = font.render(
            self.robot.kinematical_parameter_names[0] + " {0:.4f}".format(self.robot.kinematical_parameters[0]), False,
            red)  # Left
        self.screen.blit(text_surface, (30, stats_height + HEIGHT - 100))
        text_surface = font.render(
            self.robot.kinematical_parameter_names[1] + " {0:.4f}".format(self.robot.kinematical_parameters[1]), False,
            red)  # Right
        self.screen.blit(text_surface, (30, stats_height + HEIGHT - 80))
        text_surface = font.render("updates: " + str(update), False, red)
        self.screen.blit(text_surface, (30, stats_height + HEIGHT - 60))

    def draw_positions(self):
        # Positions
        text_surface = font.render("angle: {0:.2f}".format(math.degrees(self.robot.theta)), False, red)  # Angle
        self.screen.blit(text_surface, (300, stats_height + HEIGHT - 100))
        text_surface = font.render("position y: " + str(int(self.robot.y)), False, red)
        self.screen.blit(text_surface, (300, stats_height + HEIGHT - 80))
        text_surface = font.render("position x: " + str(int(self.robot.x)), False, red)
        self.screen.blit(text_surface, (300, stats_height + HEIGHT - 60))
        if self.stop:
            text_surface = font.render("use key \"p\" to resume", False, red)
        else:
            text_surface = font.render("use key \"p\" to pause", False, red)
        self.screen.blit(text_surface, (300, stats_height + HEIGHT - 40))

    def draw_performance(self):
        # Draw performance
        text_surface = font.render("not_moved: " + str(self.robot.n_not_moved), False, red)
        self.screen.blit(text_surface, (440, stats_height + HEIGHT - 100))
        text_surface = font.render("collisions: " + str(self.robot.n_collisions), False, red)
        self.screen.blit(text_surface, (440, stats_height + HEIGHT - 80))
        text_surface = font.render("cleaned_dust: " + str(self.robot.n_visited_bins), False, red)
        self.screen.blit(text_surface, (440, stats_height + HEIGHT - 60))
        text_surface = font.render("fitness: " + str(round(self.robot.fitness,2)), False, red)
        self.screen.blit(text_surface, (30, stats_height + HEIGHT - 40))

    def get_nn_weights(self):
        return self.robot.nn.flatten()

    def set_robot(self, robot):
        self.robot = robot
        self.wall_list = robot.walls

# if __name__ == '__main__':
#     pygame.init()
#     gui = GFX()
