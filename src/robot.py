import pygame


class Robot(pygame.sprite.Sprite):
	def __init__(self, WIDTH, HEIGHT, robot_size=60):
		import gui
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(gui.load_image("../images/robot.jpg", True), (robot_size, robot_size))
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH / 2
		self.rect.centery = HEIGHT / 2
		self.speed = [0.5, -0.5]
		self.width = WIDTH
		self.height = HEIGHT

	def update_position(self, time):
		self.rect.centerx += self.speed[0] * time
		self.rect.centery += self.speed[1] * time
		# TODO: For bulat, play with you physics here
		if self.rect.left <= 0 or self.rect.right >= self.width:
			# When colliding with wall on the left, rebound
			self.speed[0] = -self.speed[0]
			self.rect.centerx += self.speed[0] * time
		if self.rect.top <= 0 or self.rect.bottom >= self.height:
			# When colliding with wall on the right, rebound
			self.speed[1] = -self.speed[1]
			self.rect.centery += self.speed[1] * time
