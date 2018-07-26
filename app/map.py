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
    # todo: Maybe they meant (block_sight==None to mean is_visible==True) ?
    # one place uses `block_sight` the other "blocked_sight" so it's ambiguous
    def __init__(self, block, block_sight=None):
        self.blocked = block
        if block_sight is None:
            block_sight = block

        self.blocked_sight = block_sight


class Map:
    def __init__(self, tiles_x, tiles_y):
        self.tiles_x = tiles_x
        self.tiles_y = tiles_y
        self.init_tiles()

    def init_tiles(self):
        self.tiles = [[Tile(True) for y in range(self.tiles_y)] for x in range(self.tiles_x)]
        self.gen_static_map()
        self.gen_random_map()

    def gen_random_map(self):
        self.tiles = [[Tile(True) for y in range(self.tiles_y)] for x in range(self.tiles_x)]

    def gen_static_map(self):
        self.tiles = [[Tile(True) for y in range(self.tiles_y)] for x in range(self.tiles_x)]

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
        print(x, y)
        self.create_room(Rect(3, 4, 1, 1))
        self.create_room(Rect(7, 4, 1, 1))
        self.create_room(Rect(1, 5, 3, 3))

        x += 4
        self.create_room(Rect(x, y, 3, 3))

        self.create_tunnel_horizontal(10, 30, 30)
        self.create_tunnel_vertical(10, 30, 10)
        self.create_tunnel_horizontal(10, 30, 10)
        self.create_tunnel_vertical(10, 30, 30)

    def at(self, x, y):
        if any([x < 0,
                x > self.tiles_x,
                y < 0,
                y > self.tiles_y]):
            raise ValueError("Tile outside Map bounds: ({}, {})".format(x, y))

        return self.tiles[x][y]

    def create_room(self, rect):
        # [x1, x2), [y1, y2)
        if any([rect.x1 > rect.x2,
                rect.y1 > rect.y2]):
            print("Bad create_room args: {}".format(rect))
            return

        end_x = min(rect.x2, self.tiles_x)
        end_y = min(rect.y2, self.tiles_y)
        for x in range(rect.x1, end_x):
            for y in range(rect.y1, end_y):
                self.at(x, y).blocked = False
                self.at(x, y).blocked_sight = False

    def create_tunnel_horizontal(self, x1, x2, y):
        # naive horizontal line.
        # todo: replace with single (x1,y1)->(x2,y2) or (x1, y1, angle, length)
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.at(x, y).blocked = False
            self.at(x, y).blocked_sight = False

    def create_tunnel_vertical(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.at(x, y).blocked = False
            self.at(x, y).blocked_sight = False

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