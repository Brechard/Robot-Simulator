from src.sensor import Sensor
from src.wall import Wall
from src.helper import *

class Robot():
	def __init__(self, WIDTH, HEIGHT, walls):
		self.x = 300
		self.y = 100
		self.theta = 0
		self.radius = 30
		self.speed = [5, -5]

		self.width = WIDTH
		self.height = HEIGHT
		self.walls = walls

		self.sensors = []
		num_sensors = 12
		for i in range(num_sensors):
			self.sensors.append(Sensor(i*(360/num_sensors)))
		self.check_sensors()

	def get_pos(self):
		return int(self.x), int(self.y)

	def check_sensors(self):
		for sensor in self.sensors:
			dist = sensor.MAX_SENSOR_VALUE
			sensor_bearing = (sensor.angle + self.theta) % 360  # Sensor angle is relative to the robot
			sensor.p2 = point_from_angle(self.x, self.y, sensor_bearing, dist)
			for wall in self.walls:
				crossover = wall.intersectsLine((self.x, self.y), sensor.p2)
				if crossover != False:
					dist = distance((self.x, self.y), crossover)
					sensor.value = dist
					sensor.p2 = crossover

	def update_position(self, time):
		""" Apply the wheel velocity to the robot position using the elapsed time """
		# self.x += self.speed[0] * time
		# self.y += self.speed[1] * time
		# TODO: For bulat, play with you physics here
		# if self.rect.left <= 0 or self.rect.right >= self.width:
		# 	# When colliding with wall on the left, rebound
		# 	self.speed[0] = -self.speed[0]
		# 	self.rect.centerx += self.speed[0] * time
		# if self.rect.top <= 0 or self.rect.bottom >= self.height:
		# 	# When colliding with wall on the right, rebound
		# 	self.speed[1] = -self.speed[1]
		# 	self.rect.centery += self.speed[1] * time

		# update sensors for new pos
		self.check_sensors()
