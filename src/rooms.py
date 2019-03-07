from src.wall import Wall

WIDTH = 840
HEIGHT = 600

# Base room that contains only the outer walls
base_room = []
padding = 20
base_room.append(Wall((padding, padding), (WIDTH - padding, padding)))
base_room.append(Wall((padding, HEIGHT - padding), (WIDTH - padding, HEIGHT - padding)))
base_room.append(Wall((padding, padding), (padding, HEIGHT - padding)))
base_room.append(Wall((WIDTH - padding, padding), (WIDTH - padding, HEIGHT - padding)))


def get_base_room():
	return [wall for wall in base_room]


# Room 1 with a rectangle in the middle
room_1 = get_base_room()
padding = 230
room_1.append(Wall((padding, padding), (WIDTH - padding, padding)))
room_1.append(Wall((padding, HEIGHT - padding), (WIDTH - padding, HEIGHT - padding)))
room_1.append(Wall((padding, padding), (padding, HEIGHT - padding)))
room_1.append(Wall((WIDTH - padding, padding), (WIDTH - padding, HEIGHT - padding)))

# Room 2 with a trapezoi in the middle
room_2 = get_base_room()
room_2.append(Wall((padding * 2, padding), (WIDTH - padding, padding)))
room_2.append(Wall((padding, HEIGHT - padding), (WIDTH - padding, HEIGHT - padding)))
room_2.append(Wall((padding * 2, padding), (padding, HEIGHT - padding)))
room_2.append(Wall((WIDTH - padding, padding), (WIDTH - padding, HEIGHT - padding)))

# Room 3 with strange form
room_3 = get_base_room()
padding = 150
room_3.append(Wall((padding, padding), (WIDTH - padding, padding)))
room_3.append(Wall((padding, padding), (padding, HEIGHT - padding)))
room_3.append(Wall((WIDTH / 2, HEIGHT - padding), (WIDTH - padding, HEIGHT - padding)))
room_3.append(Wall((WIDTH / 2, HEIGHT - padding), (WIDTH / 2, HEIGHT /2)))
