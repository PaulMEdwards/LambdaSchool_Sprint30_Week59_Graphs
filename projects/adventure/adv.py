debug = False
trace = False

from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


# Room data format:
#   0: [(3, 5), {'n': 1, 's': 5, 'e': 3, 'w': 7}],
# Rm#: List containing 2 values: (x, y), Dict containing cardinal directions to connected Rm#s

# Pick a direction, going as far as you can (DFT)
# When you hit a dead end, find the nearest room with an unexplored exit (BFT/BFS)
# Goal is to build a traversal_path to visit every room

# Methods to use:
#   player.current_room.id
#   player.current_room.get_exits()
#   player.current_room.get_room_in_direction(direction)
#   player.travel(direction)


repeat_visited_rooms = []

reverse_direction = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
}

def mark_room_exits(visited_rooms, current_room, room_exits):
    visited_rooms[current_room] = {}
    for room_exit in room_exits:
        visited_rooms[current_room][room_exit] = '?'
    return visited_rooms[current_room]

def travel_dft_recursive(current_room, previous_room = None, travel_direction = None, breadcrumbs_graph = {}, visited_rooms = {}, path = []):
    global repeat_visited_rooms
    room_id = current_room.id

    room_exits = current_room.get_exits()
    exits_dictionary = mark_room_exits(visited_rooms, current_room, room_exits)
    if trace: print(f"current_room: {room_id}, exits: {room_exits}")

    breadcrumbs_graph[room_id] = exits_dictionary

    if previous_room is not None:
        path.append(travel_direction)
        breadcrumbs_graph[previous_room.id][travel_direction] = room_id
        breadcrumbs_graph[room_id][reverse_direction[travel_direction]] = previous_room.id

    for room_exit in room_exits:
        if breadcrumbs_graph[room_id][room_exit] == '?':
            target_room = current_room.get_room_in_direction(room_exit)
            if target_room not in visited_rooms:
                travel_dft_recursive(target_room, current_room, room_exit, breadcrumbs_graph, visited_rooms, path)
                path.append(reverse_direction[room_exit])
            else:
                if debug: print(f"already visited room {room_id}")
                repeat_visited_rooms.append(room_id)

    if debug: print(f"breadcrumbs_graph[{room_id}]: {breadcrumbs_graph[room_id]}")

    return path

traversal_path = travel_dft_recursive(player.current_room)

if debug: print(f"repeat_visited_rooms = {len(repeat_visited_rooms)}\n{repeat_visited_rooms}")

backtracked_rooms = []
travel_route = []

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    travel_route.append(player.current_room.id)
    player.travel(move)
    if player.current_room in visited_rooms:
        backtracked_rooms.append(player.current_room.id)
    visited_rooms.add(player.current_room)

if trace: print(f"backtracked_rooms = {len(backtracked_rooms)}\n{backtracked_rooms}")
if trace: print(f"travel_route:\n{travel_route}")

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
if not debug:
    player.current_room.print_room_description(player)
    while True:
        cmds = input("-> ").lower().split(" ")
        if cmds[0] in ["n", "s", "e", "w"]:
            player.travel(cmds[0], True)
        elif cmds[0] == "q":
            break
        else:
            print("I did not understand that command.")
