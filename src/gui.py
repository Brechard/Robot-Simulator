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
dust = (220, 225, 234)
blue = (20, 80, 155)
red = (255, 0, 0)
pygame.font.init()
font = pygame.font.SysFont('arial', 20)

# parameters
button_step = 0.05


class GFX:
    wall_list = []
    robot_size = 60

    def __init__(self, weights=None):
        # Outer walls
        padding = 20
        self.wall_list.append(Wall((padding, padding), (WIDTH - padding, padding)))
        self.wall_list.append(Wall((padding, HEIGHT - padding), (WIDTH - padding, HEIGHT - padding)))
        self.wall_list.append(Wall((padding, padding), (padding, HEIGHT - padding)))
        self.wall_list.append(Wall((WIDTH - padding, padding), (WIDTH - padding, HEIGHT - padding)))

        # padding = 230
        # self.wall_list.append(Wall((padding, padding), (WIDTH - padding, padding)))
        # self.wall_list.append(Wall((padding, HEIGHT - padding), (WIDTH - padding, HEIGHT - padding)))
        # self.wall_list.append(Wall((padding, padding), (padding, HEIGHT - padding)))
        # self.wall_list.append(Wall((WIDTH - padding, padding), (WIDTH - padding, HEIGHT - padding)))
        # self.wall_list.append(Wall((padding * 2, padding), (WIDTH - padding, padding)))
        # self.wall_list.append(Wall((padding, HEIGHT - padding), (WIDTH - padding, HEIGHT - padding)))
        # self.wall_list.append(Wall((padding * 2, padding), (padding, HEIGHT - padding)))
        # self.wall_list.append(Wall((WIDTH - padding, padding), (WIDTH - padding, HEIGHT - padding)))

        self.visited = np.zeros((WIDTH, HEIGHT))
        self.visited_arr = []

        # Init pygame window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("ARS")

        # Init robot
        self.robot = Robot(WIDTH, HEIGHT, self.wall_list, weights)

    def load_image(self, filename, transparent=False):
        try:
            image = pygame.image.load(filename).convert()
        except pygame.error as message:
            raise SystemExit(message)
        if transparent:
            color = image.get_at((0, 0))
            image.set_colorkey(color)
        return image

    def main(self, draw, max_time=100):
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

            # Draw current state
            if draw:
                self.draw()

    def event(self, events):
        if events.type == QUIT:
            sys.exit(0)
        elif events.type == KEYUP:
            if events.key == K_w:
                self.robot.speed[0] += button_step  # Left wheel increment
            elif events.key == K_s:
                self.robot.speed[0] -= button_step  # Left wheel decrement
            elif events.key == K_o:
                self.robot.speed[1] += button_step  # Right wheel increment
            elif events.key == K_l:
                self.robot.speed[1] -= button_step  # Right wheel decrement
            elif events.key == K_x:
                self.robot.speed = [0, 0]  # Set to 0
            elif events.key == K_t:
                self.robot.speed[0] += button_step  # Both increment
                self.robot.speed[1] += button_step  # Both increment
            elif events.key == K_g:
                self.robot.speed[0] -= button_step  # Both decrement
                self.robot.speed[1] -= button_step  # Both decrement

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

        self.visited_arr = self.robot.update_position()

    def draw(self):

        # Reset screen
        self.screen.fill([255, 255, 255])

        # Dust
        for visit in self.visited_arr:
            pygame.draw.circle(self.screen, dust, visit, self.robot.radius-5, 0)

        # Draw walls
        for wall in self.wall_list:
            pygame.draw.line(self.screen, black, wall.p1, wall.p2)

        # Sensors
        for i, sensor in enumerate(self.robot.sensors):
            pygame.draw.line(self.screen, red, self.robot.get_pos(), sensor.p2)
            text_surface = font.render(str(i) + ": " + "{0:.0f}".format(sensor.value), False, red)
            self.screen.blit(text_surface, sensor.p2)

        # Robot
        pygame.draw.circle(self.screen, blue, self.robot.get_pos(), self.robot.radius, 0)
        pygame.draw.line(self.screen, black, (self.robot.x, self.robot.y),
                         point_from_angle(self.robot.x, self.robot.y, self.robot.theta, self.robot.radius), 2)

        # Wheel speeds
        text_surface = font.render("left wheel: {0:.2f}".format(self.robot.speed[0]), False, red)  # Left
        self.screen.blit(text_surface, (30, HEIGHT - 100))
        text_surface = font.render("right wheel: {0:.2f}".format(self.robot.speed[1]), False, red)  # Right
        self.screen.blit(text_surface, (30, HEIGHT - 80))
        text_surface = font.render("angle: {0:.2f}".format(math.degrees(self.robot.theta)), False, red)  # Angle
        self.screen.blit(text_surface, (30, HEIGHT - 60))

        text_surface = font.render("fitness: " + str(self.robot.fitness), False, red)
        self.screen.blit(text_surface, (200, HEIGHT - 100))
        text_surface = font.render("position y: " + str(int(self.robot.y)), False, red)
        self.screen.blit(text_surface, (200, HEIGHT - 80))
        text_surface = font.render("position x: " + str(int(self.robot.x)), False, red)
        self.screen.blit(text_surface, (200, HEIGHT - 60))

        text_surface = font.render("updates: " + str(int(len(self.robot.fitness_history))), False, red)
        self.screen.blit(text_surface, (340, HEIGHT - 60))

        pygame.display.update()

    def get_nn_weights(self):
        return self.robot.nn.flatten()

    def set_robot(self, robot):
        self.robot = robot

# if __name__ == '__main__':
#     pygame.init()
#     gui = GFX()
