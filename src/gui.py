import random
import sys

import pygame
from pygame.locals import *

from robot import Robot

WIDTH = 640
HEIGHT = 480


def load_image(filename, transparent=False):
	try:
		image = pygame.image.load(filename).convert()
	except pygame.error as message:
		raise SystemExit(message)
	if transparent:
		color = image.get_at((0, 0))
		image.set_colorkey(color)
	return image


class Wall(pygame.sprite.Sprite):
	""" Wall the player can run into. """

	def __init__(self, x, y, width, height):
		""" Constructor for the wall that the player can run into. """
		# Call the parent's constructor
		super().__init__()

		# Create a color with the color specified in fill, of the size specified in the parameters
		self.image = pygame.Surface([width, height])
		self.image.fill([100, 100, 100])

		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x


def main():
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("ARS")

	clock = pygame.time.Clock()
	robot = Robot(WIDTH, HEIGHT)
	wall_list = pygame.sprite.Group()

	# Outer walls
	wall_list.add(Wall(0, 0, 2, HEIGHT))
	wall_list.add(Wall(WIDTH - 2, 0, 2, HEIGHT))
	wall_list.add(Wall(0, 0, WIDTH, 2))
	wall_list.add(Wall(0, HEIGHT - 2, WIDTH, 2))

	# Other random walls
	wall_list.add(Wall(x=WIDTH / 3, y=0, width=2, height=int(HEIGHT * random.random())))
	wall_list.add(Wall(x=int(HEIGHT * random.random()), y=0, width=2, height=int(HEIGHT * random.random())))
	wall_list.add(
		Wall(x=int(HEIGHT * random.random()), y=int(HEIGHT * random.random()), width=int(WIDTH * random.random()),
			 height=2))

	# background = load_image("../images/background.png")

	while True:
		time = clock.tick(60)
		for events in pygame.event.get():
			if events.type == QUIT:
				sys.exit(0)

		robot.update_position(time)
		# screen.blit(background, (0, 0))
		screen.fill([255, 255, 255])
		wall_list.draw(screen)
		screen.blit(robot.image, robot.rect)
		pygame.display.flip()
	return 0


if __name__ == '__main__':
	pygame.init()
	main()
