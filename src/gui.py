import sys
from datetime import datetime

import pygame
from pygame.locals import *
import numpy as np

from neuralnet import *
from src.helper import *
from src.robot import Robot
from src.wall import Wall

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
yellow = (255, 255, 0)
green_sensor = (53, 98, 68)
stats_height = 80
pygame.font.init()
font = pygame.font.SysFont('arial', 20)

# parameters
button_step = 0.05


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

    def add_beacons(self, n_random_beacons=10):
        beacons = []
        beacon_step = 200
        for i in range(int(WIDTH/beacon_step) + 1):
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

    def main(self, draw, kill_when_stuck=False, max_time=100):
        clock = pygame.time.Clock()
        # background = load_image("../images/background.png")
        if not draw:
            pygame.display.iconify()

        self.start_time = datetime.now()
        self.last_time = datetime.now()

        for i in range(max_time):
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
                self.robot.kinematical_parameters[1] -= button_step / 100  # Decrement angular velocity
            elif events.key == K_d:
                self.robot.kinematical_parameters[1] += button_step / 100  # Increment angular velocity

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

        for state in self.robot.predictions:
            pygame.draw.circle(self.screen, red, [int(x) for x in state[:2]], 2, 0)

        for state in self.robot.believe_states:
            pygame.draw.circle(self.screen, dust, [int(x) for x in state[:2]], 2, 0)

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

        pygame.display.update()

    def draw_kinematics(self, update):

        # Wheel speeds
        text_surface = font.render(
            self.robot.kinematical_parameter_names[0] + " {0:.4f}".format(self.robot.kinematical_parameters[0]), False,
            red)  # Left
        self.screen.blit(text_surface, (30, stats_height + HEIGHT - 80))
        text_surface = font.render(
            self.robot.kinematical_parameter_names[1] + " {0:.4f}".format(self.robot.kinematical_parameters[1]), False,
            red)  # Right
        self.screen.blit(text_surface, (30, stats_height + HEIGHT - 60))
        text_surface = font.render("updates: " + str(update), False, red)
        self.screen.blit(text_surface, (30, stats_height + HEIGHT - 40))

    def draw_positions(self):
        # Positions
        text_surface = font.render("angle: {0:.2f}".format(math.degrees(self.robot.theta)), False, red)  # Angle
        self.screen.blit(text_surface, (300, stats_height + HEIGHT - 80))
        text_surface = font.render("position y: " + str(int(self.robot.y)), False, red)
        self.screen.blit(text_surface, (300, stats_height + HEIGHT - 60))
        text_surface = font.render("position x: " + str(int(self.robot.x)), False, red)
        self.screen.blit(text_surface, (300, stats_height + HEIGHT - 40))

    def draw_performance(self):
        # Draw performance
        text_surface = font.render("not_moved: " + str(self.robot.n_not_moved), False, red)
        self.screen.blit(text_surface, (440, stats_height + HEIGHT - 80))
        text_surface = font.render("collisions: " + str(self.robot.n_collisions), False, red)
        self.screen.blit(text_surface, (440, stats_height + HEIGHT - 60))
        text_surface = font.render("cleaned_dust: " + str(self.robot.n_visited_bins), False, red)
        self.screen.blit(text_surface, (440, stats_height + HEIGHT - 40))
        text_surface = font.render("fitness: " + str(self.robot.fitness), False, red)
        self.screen.blit(text_surface, (600, stats_height + HEIGHT - 80))

    def get_nn_weights(self):
        return self.robot.nn.flatten()

    def set_robot(self, robot):
        self.robot = robot
        self.wall_list = robot.walls

# if __name__ == '__main__':
#     pygame.init()
#     gui = GFX()
