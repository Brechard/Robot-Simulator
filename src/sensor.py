

class Sensor():
	MAX_SENSOR_VALUE = 200

	def __init__(self, angle):
		self.angle = angle
		self.value = self.MAX_SENSOR_VALUE
		self.p2 = None