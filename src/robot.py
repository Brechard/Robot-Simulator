from src.sensor import Sensor
from src.wall import Wall
from src.helper import *

class Robot():
	def __init__(self, WIDTH, HEIGHT, walls):
		self.x = 100
		self.y = 200
		self.theta = 10
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
			sensor_bearing = (sensor.angle + self.theta) % 360  # Sensor angle is relative to the robot
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

				self.check_sensors()

	def update_position(self, time):
		""" Apply the wheel velocity to the robot position using the elapsed time """
		self.x += self.speed[0] * time
		self.y += self.speed[1] * time

		self.theta += time*5
		if self.theta > 360:
			self.theta = 0
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
