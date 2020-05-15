from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# utils
class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)


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
traversal_path = []
mygraph = {}

def opposite(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    elif direction == 'w':
        return 'e'


def bfs_path(graph, start_room):
    queue = Queue()
    queue.enqueue([start_room])
    visited = set()

    while queue.size():
        path = queue.dequeue()
        vert_room = path[-1]
        if vert_room not in visited:
            visited.add(vert_room)
            for room_exit in graph[vert_room]:
                if graph[vert_room][room_exit] == '?':
                    return path
            for v in graph[vert_room]:
                adjacent_room = graph[vert_room][v]
                new_path = list(path)
                new_path.append(adjacent_room)
                queue.enqueue(new_path)
    return None

while len(mygraph) < len(room_graph):
    current = player.current_room.id
    if current not in mygraph:
        exits = player.current_room.get_exits()
        mygraph[current] = {i: '?' for i in exits}
        
    room_exit = None
    for direction in mygraph[current]:
        if mygraph[current][direction] == '?':
            room_exit = direction
            if room_exit is not None:
                traversal_path.append(room_exit)
                player.travel(room_exit)
                # discovered = player.current_room.id

                if player.current_room.id not in mygraph:
                    exits = player.current_room.get_exits()
                    mygraph[player.current_room.id] = {i: '?' for i in exits}

            mygraph[current][room_exit] = player.current_room.id
            mygraph[player.current_room.id][opposite(room_exit)] = current  # the value of current
            current = player.current_room.id  # current is now the value of discovered
            break

    # if there are no unexplored question marks
    rooms = bfs_path(mygraph, player.current_room.id)
    print('rooms', rooms)
    if rooms is not None:
        for room in rooms:
            for direction in mygraph[current]:
                if mygraph[current][direction] == room:
                    traversal_path.append(direction)
                    player.travel(direction)
            current = player.current_room.id





# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")

