import random
import sys
from datetime import datetime
import math

import pygame
from pygame.locals import *

from src.robot import Robot
from src.wall import Wall
from src.helper import *

WIDTH = 1040
HEIGHT = 600

# some colors
black = (0, 0, 0)
blue = (20, 80, 155)
red = (255, 0, 0)
pygame.font.init()
font = pygame.font.SysFont('arial', 20)


class GFX:
    wall_list = []
    robot_size = 60

    def __init__(self):
        # Outer walls
        padding = 20
        self.wall_list.append(Wall((padding, padding), (WIDTH - padding, padding)))
        self.wall_list.append(Wall((padding, HEIGHT - padding), (WIDTH - padding, HEIGHT - padding)))
        self.wall_list.append(Wall((padding, padding), (padding, HEIGHT - padding)))
        self.wall_list.append(Wall((WIDTH - padding, padding), (WIDTH - padding, HEIGHT - padding)))

        padding = 200
        self.wall_list.append(Wall((padding, padding), (WIDTH - padding, padding)))
        self.wall_list.append(Wall((padding, HEIGHT - padding), (WIDTH - padding, HEIGHT - padding)))
        self.wall_list.append(Wall((padding, padding), (padding, HEIGHT - padding)))
        self.wall_list.append(Wall((WIDTH - padding, padding), (WIDTH - padding, HEIGHT - padding)))

        # Other random walls
        # wall_list.add(Wall(x=WIDTH / 3, y=0, width=2, height=int(HEIGHT * random.random())))
        # wall_list.add(Wall(x=int(HEIGHT * random.random()), y=0, width=2, height=int(HEIGHT * random.random())))
        # wall_list.add(
        # 	Wall(x=int(HEIGHT * random.random()), y=int(HEIGHT * random.random()), width=int(WIDTH * random.random()),
        # 		 height=2))

        # Init pygame window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("ARS")

        # Init robot
        self.robot = Robot(WIDTH, HEIGHT, self.wall_list)

        self.main()

    def load_image(self, filename, transparent = False):
        try:
            image = pygame.image.load(filename).convert()
        except pygame.error as message:
            raise SystemExit(message)
        if transparent:
            color = image.get_at((0, 0))
            image.set_colorkey(color)
        return image

    def main(self):
        clock = pygame.time.Clock()
        # background = load_image("../images/background.png")

        self.start_time = datetime.now()
        self.last_time = datetime.now()

        while True:
            # Handle inputs
            for events in pygame.event.get():
                self.event(events)

            # Update state
            self.update()

            # Draw current state
            self.draw()

    def event(self, events):
        if events.type == QUIT:
            sys.exit(0)
        elif events.type == KEYUP:
            # TODO: add controls here
            if events.key == K_w:
                self.robot.speed[0] += 1  # Left wheel increment (todo: apply max velocity)
            elif events.key == K_s:
                self.robot.speed[0] -= 1  # Left wheel decrement
            elif events.key == K_o:
                self.robot.speed[1] += 1  # Right wheel increment
            elif events.key == K_l:
                self.robot.speed[1] -= 1  # Right wheel decrement
            elif events.key == K_x:
                self.robot.speed = [0, 0]  # Set to 0
            elif events.key == K_t:
                self.robot.speed[0] += 1  # Both increment
                self.robot.speed[1] += 1  # Both increment
            elif events.key == K_g:
                self.robot.speed[0] -= 1  # Both decrement
                self.robot.speed[1] -= 1  # Both decrement

    def update(self):
        # Update robot step
        now = datetime.now()
        time_diff = now - self.last_time
        time_diff = time_diff.total_seconds()
        self.last_time = now

        self.robot.update_position_test()

    # Check wall intersections
    # for wall in self.wall_list:
    # 	intersect = wall.intersectsRobot(self.robot.x, self.robot.y, self.robot.radius)
    # 	if intersect is not None and len(intersect) > 0:
    # 		t=2

    def draw(self):

        # Reset screen
        self.screen.fill([255, 255, 255])

        # Draw walls
        for wall in self.wall_list:
            pygame.draw.line(self.screen, black, wall.p1, wall.p2)

        # Sensors
        for i, sensor in enumerate(self.robot.sensors):
            pygame.draw.line(self.screen, red, self.robot.get_pos(), sensor.p2)
            textsurface = font.render(str(i) + ": " + "{0:.0f}".format(sensor.value), False, red)
            self.screen.blit(textsurface, sensor.p2)

        # Robot
        pygame.draw.circle(self.screen, blue, self.robot.get_pos(), self.robot.radius, 0)
        pygame.draw.line(self.screen, black, (self.robot.x, self.robot.y),
                         point_from_angle(self.robot.x, self.robot.y, self.robot.theta, self.robot.radius), 2)

        # Wheel speeds
        textsurface = font.render("left wheel: {0:.0f}".format(self.robot.speed[0]), False, red)  # Left
        self.screen.blit(textsurface, (30, HEIGHT - 100))
        textsurface = font.render("rigth wheel: {0:.0f}".format(self.robot.speed[1]), False, red)  # Right
        self.screen.blit(textsurface, (30, HEIGHT - 80))
        textsurface = font.render("angle: {0:.2f}".format(math.degrees(self.robot.theta)), False, red)  # Angle
        self.screen.blit(textsurface, (30, HEIGHT - 60))

        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    gui = GFX()
