
class Sensor:
	MAX_SENSOR_VALUE = 100

	def __init__(self, angle):
		self.angle = angle
		self.value = self.MAX_SENSOR_VALUE
		self.p2 = None