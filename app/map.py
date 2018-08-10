from enum import Enum, unique
import logging
from random import randint
import time

from app import colors

ROOM_MAX_SIZE = 9
ROOM_MIN_SIZE = 3
ROOMS_MAX = 20
ROOMS_MAX_FAILURES = 20
ROOMS_MAX_TIMEOUT_SECS = .6
ROOMS_MAX_MONSTERS = 4

@unique
class TileId(Enum):
    WALL = 0
    FLOOR = 1
    GRASS = 2
    RANDOM = 999


class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def get_center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return (center_x, center_y)

    def width(self):
        return self.x2 - self.x1

    def height(self):
        return self.y2 - self.y1

    def in_rect(self, other):
        return (
            self.x1 >= other.x1 and self.x1 <= other.x2 and
            self.x2 >= other.x1 and self.x2 <= other.x2 and
            self.y1 >= other.y1 and self.y1 <= other.y2 and
            self.y2 >= other.y1 and self.y2 <= other.y2
        )

    def intersect(self, other, padding=0):
        # off-by-one error, see Map() create_room
        if padding >= 0:
            return (self.x1 - padding < other.x2 and self.x2 + padding > other.x1 and
                    self.y1 - padding < other.y2 and self.y2 + padding > other.y1)
        else:
            return (self.x1 < other.x2 and self.x2 > other.x1 and
                    self.y1 < other.y2 and self.y2 > other.y1)

    def __str__(self):
        return "Rect(x1={}, y1={}, x2={}, y2={})".format(self.x1, self.y1, self.x2, self.y2)


class Tile:
    # default to block both if block=True
    def __init__(self, tile_id, blocking=False):
        self.blocking = blocking
        self.color = colors.white
        self.tile_id = TileId.FLOOR
        self.explored = False
        self.blocks_vision = False
        self.set_type(tile_id)

    def set_type(self, tile_id):
        self.tile_id = tile_id
        self.blocking = False

        if tile_id is TileId.FLOOR:
            self.color = colors.dark_floor
        elif tile_id is TileId.WALL:
            self.blocking = True
            self.blocks_vision = True
            self.color = colors.dark_wall
        elif tile_id is TileId.GRASS:
            self.color = colors.dark_green
        # elif tile_id is TileId.RANDOM:
        #     self.color = colors.random_color()
        else:
            raise ValueError("Unknown tile type: {}".format(tile_id))


class Map:
    def __init__(self, tiles_x, tiles_y, game):
        self.tiles_x = tiles_x
        self.tiles_y = tiles_y
        self.reset(self.tiles_x, self.tiles_y)
        self.tiles = [[]]
        self.game = game
        self.debug_show_colors = True
        self.room_gen_padding = 0

    def reset(self, tiles_x, tiles_y, tile_id=None):
        if tile_id is None:
            tile_id = TileId.WALL
        self.tiles_x = tiles_x
        self.tiles_y = tiles_y
        self.tiles = [[Tile(tile_id) for y in range(self.tiles_y)] for x in range(self.tiles_x)]

    def gen_random_map(self):
        self.reset(self.tiles_x, self.tiles_y, tile_id=TileId.WALL)

        rect_map = Rect(0, 0, self.tiles_x, self.tiles_y)
        rooms = []
        room_id = 0
        time_start = time.time()

        while room_id < ROOMS_MAX and time.time() - time_start <= ROOMS_MAX_TIMEOUT_SECS:
            room = Rect(
                x=randint(0, self.tiles_x),
                y=randint(0, self.tiles_y),
                w=randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE),
                h=randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE),
            )
            logging.info("Room [{}] = {}".format(room_id, room))

            if not room.in_rect(rect_map):
                continue

            valid_room = True
            for other in rooms:
                if room.intersect(other, padding=self.room_gen_padding):
                    valid_room = False
                    logging.debug("\tcollide: \t{}".format(other))
                    logging.debug("\tself: \t\t{}".format(room))
                    break

            if valid_room:
                rooms.append(room)
                room_id += 1
                # name rooms using letters
                self.game.spawn('debug', **{
                    'char': 32+room_id,
                    'x': room.x1,
                    'y': room.y1})

        for room in rooms:
            if self.debug_show_colors:
                self.create_room(room, tile_id=TileId.FLOOR, color=colors.random_color())
            else:
                self.create_room(room, tile_id=TileId.FLOOR, color=None)

        for counter, room in enumerate(rooms):
            if counter == 0:
                self.game.spawn('player', **{
                    'x': room.get_center()[0],
                    'y': room.get_center()[1]})
                continue
            else:
                monsters = randint(0, ROOMS_MAX_MONSTERS)
                for _ in range(monsters):
                    self.game.spawn('monster', **{
                        'x': randint(room.x1, room.x2 - 1),
                        'y': randint(room.y1, room.y2 - 1)})

            prev_room = rooms[counter-1]
            pos_prev = prev_room.get_center()
            pos_room = room.get_center()

            if randint(0, 1):
                self.create_tunnel_horizontal(pos_prev[0], pos_room[0], pos_prev[1])
                self.create_tunnel_vertical(pos_prev[1], pos_room[1], pos_room[0])
            else:
                self.create_tunnel_vertical(pos_prev[1], pos_room[1], pos_prev[0])
                self.create_tunnel_horizontal(pos_prev[0], pos_room[0], pos_room[1])

        logging.info("Rooms used: {}".format(len(rooms)))

    def gen_static_map(self):
        self.reset(self.tiles_x, self.tiles_y)
        r1 = Rect(20, 15, 10, 15)
        r2 = Rect(50, 15, 10, 15)
        self.create_room(r1)
        self.create_room(r2)
        self.create_tunnel_horizontal(25, 55, 23)

        self.game.spawn('player', **{
            'x': r1.get_center()[0],
            'y': r1.get_center()[1]})

        self.game.spawn('monster', **{
            'x': r2.get_center()[0],
            'y': r2.get_center()[1]})

    def in_bounds(self, x, y):
        # is tile on map
        if any([x < 0,
                x >= self.tiles_x,
                y < 0,
                y >= self.tiles_y]):
            return False

        return True

    def tile_is_visible(self, x, y):
        if not self.in_bounds(x, y):
            return False

        if self.at(x, y).blocking:
            return False

        # todo: LOS test
        # if self.at(x, y).blocks_vision:
        #     return False

        return True

    def at(self, x, y):
        if self.in_bounds(x, y):
            return self.tiles[x][y]
        else:
            raise ValueError("Tile ({}, {}) outside of bounds: {}".format(x, y, self))

    def create_room(self, rect, tile_id=None, color=None):
        if tile_id is None:
            tile_id = TileId.FLOOR

        # [x1, x2), [y1, y2)
        if any([rect.x1 > rect.x2,
                rect.y1 > rect.y2]):
            logging.warning("Bad create_room() args: {}".format(rect))
            return

        end_x = min(rect.x2, self.tiles_x)
        end_y = min(rect.y2, self.tiles_y)
        for x in range(rect.x1, end_x):
            for y in range(rect.y1, end_y):
                self.at(x, y).set_type(tile_id)
                if color is not None:
                    self.at(x, y).color = color

    def create_tunnel_horizontal(self, x1, x2, y, tile_id=None):
        # naive horizontal line.
        if tile_id is None:
            tile_id = TileId.FLOOR

        # todo: replace with single (x1,y1)->(x2,y2) or (x1, y1, angle, length)
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.at(x, y).set_type(tile_id)

    def create_tunnel_vertical(self, y1, y2, x, tile_id=None):
        # todo: replace this and create_tunnel_horizontal()
        if tile_id is None:
            tile_id = TileId.FLOOR

        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.at(x, y).set_type(tile_id)

    def is_blocked(self, x, y):
        # default to failed bounds check
        if x < 0 or x >= self.tiles_x:
            return True

        if y < 0 or y >= self.tiles_y:
            return True

        if self.at(x,y).blocking:
            return True

        return False

    def __str__(self):
        return "Map({}, {})".format(self.tiles_x, self.tiles_y)