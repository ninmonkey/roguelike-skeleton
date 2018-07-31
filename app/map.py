from enum import Enum, unique

from random import randint
from app import colors

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
ROOMS_MAX = 30
ROOMS_MAX_FAILURES = 20

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

    def in_rect(self, other):
        return (
            self.x1 >= other.x1 and self.x1 <= other.x2 and
            self.x2 >= other.x1 and self.x2 <= other.x2 and
            self.y1 >= other.y1 and self.y1 <= other.y2 and
            self.y2 >= other.y1 and self.y2 <= other.y2
        )

    def intersect(self, other):
        # off-by-one error, see Map() create_room
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

    def __str__(self):
        return "Rect(x1={}, y1={}, x2={}, y2={})".format(self.x1, self.y1, self.x2, self.y2)


class Tile:
    # default to block both if block=True
    def __init__(self, tile_id, blocking=False):
        self.blocking = blocking
        self.color = colors.white
        self.value = 0
        self.set_type(tile_id)

    def set_type(self, tile_id):
        self.value = tile_id.value
        self.blocking = False

        if tile_id is TileId.FLOOR:
            self.color = colors.dark_floor
        elif tile_id is TileId.WALL:
            self.blocking = True
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

    def reset(self, tiles_x, tiles_y, tile_id=None):
        if tile_id is None:
            tile_id = TileId.WALL
        self.tiles_x = tiles_x
        self.tiles_y = tiles_y
        self.tiles = [[Tile(tile_id) for y in range(self.tiles_y)] for x in range(self.tiles_x)]

    def gen_random_map(self):
        self.reset(self.tiles_x, self.tiles_y, tile_id=TileId.WALL)

        r1 = Rect(
            x=randint(0, self.tiles_x),
            y=randint(0, self.tiles_y),
            w=randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE),
            h=randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE),
        )
        rect_screen = Rect(0, 0, self.tiles_x, self.tiles_y)
        rooms = []
        # print(rect_screen)
        # print(r1)
        # if not r1.intersect(rect_screen):
        #     print("Warning: room outside map!")

        for room_id in range(1):
            room = Rect(
                x=randint(0, self.tiles_x),
                y=randint(0, self.tiles_y),
                w=randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE),
                h=randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE),
            )
            print(room)
            print(rect_screen)
            if not room.in_rect(rect_screen):
                print("bad")
            else:
                print("good")
                rooms.append(room)


            self.create_room(room, tile_id=TileId.FLOOR, color=colors.random_color())


            # self.game.spawn('player', **{
            #     'x': r1.get_center()[0],
            #     'y': r1.get_center()[1]})

    def test_gen_random_map(self):
        self.reset(self.tiles_x, self.tiles_y)
        x=randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        r1 = Rect(
            x=x,
            y=2,
            w=4,
            h=4
        )
        r2 = Rect(
            x=r1.x2,
            y=r1.y1,
            w=4,
            h=4
        )
        r3 = Rect(
            x=r1.x2,
            y=r1.y1 + 4,
            w=4,
            h=4
        )
        r4 = Rect(
            x=r1.x1,
            y=r1.y1 + 4,
            w=4,
            h=4
        )
        self.create_room(r1, tile_id=TileId.FLOOR, color=colors.random_color())
        self.create_room(r2, tile_id=TileId.FLOOR, color=colors.random_color())
        self.create_room(r3, tile_id=TileId.FLOOR, color=colors.random_color())
        self.create_room(r4, tile_id=TileId.FLOOR, color=colors.random_color())

        print(r1)
        print(r4)
        print(r1.intersect(r4))
        print(r4.intersect(r1))

        print(r1)
        print(r2)
        print(r1.intersect(r2))
        print(r2.intersect(r1))

        print(r3)
        print(r4)
        print(r3.intersect(r3))
        print(r4.intersect(r4))

        self.game.spawn('player', **{
            'x': r1.get_center()[0],
            'y': r1.get_center()[1]})

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
                x > self.tiles_x,
                y < 0,
                y > self.tiles_y]):
            return False

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
            print("Bad create_room() args: {}".format(rect))
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