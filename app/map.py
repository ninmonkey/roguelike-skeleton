ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
ROOMS_MAX = 30
ROOMS_MAX_FAILURES = 20


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

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

    def __str__(self):
        return "Rect(x1={}, y1={}, x2={}, y2={})".format(self.x1, self.y1, self.x2, self.y2)


class Tile:
    # default to block both if block=True
    def __init__(self, block, visible=None):
        self.blocked = block
        if visible is None:
            visible = block

        self.visible = visible


class Map:
    def __init__(self, tiles_x, tiles_y, game):
        self.tiles_x = tiles_x
        self.tiles_y = tiles_y
        self.reset(self.tiles_x, self.tiles_y)
        # self.init_tiles()
        # self.tiles = [[]]
        self.game = game

    def reset(self, tiles_x, tiles_y):
        self.tiles_x = tiles_x
        self.tiles_y = tiles_y
        self.tiles = [[Tile(True) for y in range(self.tiles_y)] for x in range(self.tiles_x)]

    # def init_tiles(self):
    #     self.reset(self.tiles_x, self.tiles_y)
        # self.tiles = [[Tile(True) for y in range(self.tiles_y)] for x in range(self.tiles_x)]
        # self.gen_static_map()
        # self.gen_random_map()

    def gen_random_map(self):
        self.reset(self.tiles_x, self.tiles_y)
        r1 = Rect(20, 15, 10, 15)
        r2 = Rect(50, 15, 10, 15)
        self.create_room(r1)
        self.create_room(r2)
        self.create_tunnel_horizontal(25, 55, 23)

    def gen_static_map(self):
        self.reset(self.tiles_x, self.tiles_y)
        print(self)

        # rooms connected by doors
        x = self.tiles_x//2
        y = self.tiles_y//2

        self.create_room(Rect(0, 0, 1, 2))

        x = 1
        y = 1
        self.create_room(Rect(x, y, 3, 3))
        self.create_room(Rect(x+3, y, 1, 1))

        x += 4
        self.create_room(Rect(x, y, 3, 3))

        x -= 4
        y += 4
        self.create_room(Rect(3, 4, 1, 1))
        self.create_room(Rect(7, 4, 1, 1))
        self.create_room(Rect(1, 5, 3, 3))

        x += 4
        self.create_room(Rect(x, y, 3, 3))

        self.create_tunnel_horizontal(10, 30, 30)
        self.create_tunnel_vertical(10, 30, 10)
        self.create_tunnel_horizontal(10, 30, 10)
        self.create_tunnel_vertical(10, 30, 30)

        r = Rect(18, 18, 5, 5)
        self.create_room(r)
        self.game.player.teleport_to(*r.get_center())

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

    def create_room(self, rect):
        # [x1, x2), [y1, y2)
        if any([rect.x1 > rect.x2,
                rect.y1 > rect.y2]):
            print("Bad create_room() args: {}".format(rect))
            return

        end_x = min(rect.x2, self.tiles_x)
        end_y = min(rect.y2, self.tiles_y)
        for x in range(rect.x1, end_x):
            for y in range(rect.y1, end_y):
                self.at(x, y).blocked = False
                self.at(x, y).visible = False

    def create_tunnel_horizontal(self, x1, x2, y):
        # naive horizontal line.
        # todo: replace with single (x1,y1)->(x2,y2) or (x1, y1, angle, length)
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.at(x, y).blocked = False
            self.at(x, y).visible = False

    def create_tunnel_vertical(self, y1, y2, x):
        # todo: replace this and create_tunnel_horizontal()
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.at(x, y).blocked = False
            self.at(x, y).visible = False

    def is_blocked(self, x, y):
        # default to failed bounds check
        if x < 0 or x >= self.tiles_x:
            return True

        if y < 0 or y >= self.tiles_y:
            return True

        if self.at(x,y).blocked:
            return True

        return False

    def __str__(self):
        return "Map({}, {})".format(self.tiles_x, self.tiles_y)