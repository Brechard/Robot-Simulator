class Wall():
	""" Wall the player can run into. """

	def __init__(self, p1, p2):
		""" Constructor for the wall that the player can run into. """
		self.p1 = p1
		self.p2 = p2

	def intersectsLine(self, line2_p1, line2_p2):
		""" If the given line intersects the wall, returns the position of this intersection """
		# Todo: find a library for this

		# Check if lines intersect
		if self.p1[0] > line2_p1[0] and self.p1[0] > line2_p2[0] and self.p2[0] > line2_p1[0] and self.p2[0] > line2_p2[
			0]: return False
		if self.p1[0] < line2_p1[0] and self.p1[0] < line2_p2[0] and self.p2[0] < line2_p1[0] and self.p2[0] < line2_p2[
			0]: return False
		if self.p1[1] > line2_p1[1] and self.p1[1] > line2_p2[1] and self.p2[1] > line2_p1[1] and self.p2[1] > line2_p2[
			1]: return False
		if self.p1[1] < line2_p1[1] and self.p1[1] < line2_p2[1] and self.p2[1] < line2_p1[1] and self.p2[1] < line2_p2[
			1]: return False

		# Get diffs along each axis
		x_diff = (self.p1[0] - self.p2[0], line2_p1[0] - line2_p2[0])
		y_diff = (self.p1[1] - self.p2[1], line2_p1[1] - line2_p2[1])

		def det(a, b):
			return a[0] * b[1] - a[1] * b[0]

		# Find the intersection
		div = det(x_diff, y_diff)
		if div == 0: return False
		d = (det(*(self.p1, self.p2)), det(*(line2_p1, line2_p2)))
		x = det(d, x_diff) / div
		y = det(d, y_diff) / div

		# Check if intersection exceeds the segments
		margin = 0.0001
		if (x < min(self.p1[0], self.p2[0]) - margin or
				x > max(self.p1[0], self.p2[0]) + margin or
				y < min(self.p1[1], self.p2[1]) - margin or
				y > max(self.p1[1], self.p2[1]) + margin or
				x < min(line2_p1[0], line2_p2[0]) - margin or
				x > max(line2_p1[0], line2_p2[0]) + margin or
				y < min(line2_p1[1], line2_p2[1]) - margin or
				y > max(line2_p1[1], line2_p2[1]) + margin):
			return False

		return x, y

	def intersectsRobot(self, x, y, radius):
		""" Returns the position at which the robot intersects the wall, if there is one """
		# intersect = intersection(self.line, Circle(Point(x, y), radius))
		t = 2
