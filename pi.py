# pi = C / d
# pi = C when d = 1

from math import sin as sinr, radians, pi
from time import sleep
sin = lambda a: sinr(radians(a))

def get_inner_circumference(sides):
	inner_angle = 360 / sides
	other_angles = (180 - inner_angle) / 2
	side = (sin(inner_angle) * 0.5) / sin(other_angles)
	return side * sides


def get_outer_circumference(sides):
	inner_angle = 360 / sides
	other_angles = (180 - inner_angle) / 2
	cross_bar = get_inner_circumference(sides) / sides
	other_angles = 90 - other_angles
	vertex_angle = 180 - (2 * other_angles)
	half_side = (sin(other_angles) * cross_bar) / sin(vertex_angle)
	return half_side * sides * 2


def get_circumference(sides):
	inner = get_inner_circumference(sides)
	outer = get_outer_circumference(sides)
	return (inner + outer) / 2


if __name__ == "__main__":
	for i in range(12824):
		estimation = get_circumference(i + 3)
		accuracy = (1 - (abs(estimation - pi) / pi)) * 100
		print("{}: {:10f}%".format(estimation, accuracy))