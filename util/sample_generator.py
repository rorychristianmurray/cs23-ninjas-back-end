# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.
import random
from room_generator import ProceduralContent

# pseduo code for adding
pc = ProceduralContent()
listy = pc.generator()
# print(listy)
randomSel = random.randint(0, len(listy))
listy[randomSel]['name']
listy[randomSel]['desc']
listy.pop(randomSel)


class Room:
    def __init__(self, id, name, description, x, y, n=0, s=0, e=0, w=0):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = n
        self.s_to = s
        self.e_to = e
        self.w_to = w
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.x}"

    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        if direction == "n":
            self.n_to = connecting_room.id
            connecting_room.s_to = self.id
        elif direction == "s":
            self.s_to = connecting_room.id
            connecting_room.n_to = self.id
        elif direction == "e":
            self.e_to = connecting_room.id
            connecting_room.w_to = self.id
        else:
            self.w_to = connecting_room.id
            connecting_room.e_to = self.id

    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0

    def generate_rooms(self, size_x, size_y, num_rooms):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        # Start from lower-left corner (0,0)
        x = -1  # (this will become 0 on the first step)
        y = 0
        room_count = 1

        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west

        # While there are rooms to be created...
        previous_room = None
        while room_count < num_rooms:

            # Calculate the direction of the room to be created
            if direction > 0 and x < size_x - 1:
                room_direction = "e"
                x += 1
            elif direction < 0 and x > 0:
                room_direction = "w"
                x -= 1
            else:
                # If we hit a wall, turn north and reverse direction
                room_direction = "n"
                y += 1
                direction *= -1

            # Create a room in the given direction
            randomSel = random.randint(0, len(listy))
            name = listy[randomSel]['name']
            desc = listy[randomSel]['desc']
            listy.pop(randomSel)
            room = Room(room_count, name,
                        desc, x, y)
            # Note that in Django, you'll need to save the room after you create it

            # Save the room in the World grid
            self.grid[y][x] = room

            # Connect the new room to the previous room
            if previous_room is not None:
                previous_room.connect_rooms(room, room_direction)

            # Update iteration variables
            previous_room = room
            room_count += 1

    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid)  # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)

    def gen_fixture(self):
        """
        Generates create_world fixture
        """
        # Flatten grid of rooms
        flat_list = [item for sublist in self.grid for item in sublist]
        formatted_fixture = []
        for i, room in enumerate(flat_list, start=0):
            if room is None:
                continue
            formatted_room = {}
            formatted_room["model"] = 'adventure.room'
            formatted_room["pk"] = room.id
            formatted_room["fields"] = {
                "title": room.name,
                "description": room.description,
                "n_to": room.n_to,
                "s_to": room.s_to,
                "e_to": room.e_to,
                "w_to": room.w_to,
                "x": room.x,
                "y": room.y,
            }
            formatted_fixture.append(formatted_room)
        f = open('generated_world.json', "w+")
        f.write(str(formatted_fixture))
        f.close()


w = World()
num_rooms = 100
width = 12
height = 10
w.generate_rooms(width, height, num_rooms)
# w.print_rooms()
w.gen_fixture()


print(
    f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
