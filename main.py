import os
import random

# import tcod as libtcod
import tdl

from app import colors
from app.render import (
    render_blit,
    render_clear_all,
    render_entities,
)

LIMIT_FPS = 20
PATH_APP_ROOT = os.path.dirname(os.path.abspath(__file__))


class Map:
    def __init__(self, tiles_x, tiles_y):
        self.tiles_x = tiles_x
        self.tiles_y = tiles_y
        self.init_tiles()

    def init_tiles(self):
        self.tiles = [[Tile(True) for y in range(self.tiles_y)] for x in range(self.tiles_x)]

        # two rooms connected by door
        self.create_room(Rect(20, 20, 30, 8))
        self.create_room(Rect(self.tiles_x//2, self.tiles_y//2,  2, 4))
        self.create_room(Rect(20, 28, 30, 8))

        self.create_room(Rect(0, 0, 4, 2))
        self.create_room(Rect(0, 2, 2, 2))

    def create_room(self, rect):
        for x in range(rect.x1 + 1, min(rect.x2, self.tiles_x)):
            for y in range(rect.y1 + 1, min(rect.y2, self.tiles_y)):
                print(x, y)
                self.tiles[x][y].blocked = False
                self.tiles[x][y].blocked_sight = False

    def is_blocked(self, x, y):
        # default to failed bounds check
        if x < 0 or x >= self.tiles_x:
            return True

        if y < 0 or y >= self.tiles_y:
            return True

        if self.tiles[x][y].blocked:
            return True

        return False


class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h


class Tile:
    # default to block both if block=True
    def __init__(self, block, block_sight=None):
        self.blocked = block
        if block_sight is None:
            block_sight = block

        self.blocked_sight = block_sight


class Entity:
    def __init__(self, x, y, char, color, map):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.map = map

    def move(self,  dx, dy):
        if not self.map.is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy


class Game:
    """
    members:
        root_console: main screen surface
        con: 2nd surface, back-buffer to render to root_console
    """
    def __init__(self):
        self.init()
        # path = random_font_path()
        path = os.path.join(PATH_APP_ROOT, 'fonts', 'arial10x10.png')
        tdl.set_font(path, greyscale=True, altLayout=True)
        self.root_console = tdl.init(self.TILES_X, self.TILES_Y, title='tcod demo', fullscreen=False)
        self.con = tdl.Console(self.TILES_X, self.TILES_Y)
        tdl.setFPS(LIMIT_FPS)

    def init(self):
        # reset for next round
        self.is_done = False
        self.TILES_X = 80
        self.TILES_Y = 50

        self.map = Map(self.TILES_X, self.TILES_Y)

        player_x = self.TILES_X // 2
        player_y = self.TILES_Y // 2
        self.player = Entity(player_x, player_y, '@', colors.white, self.map)

        monster = Entity(self.player.x - 2, self.player.y, '@', colors.yellow, self.map)
        self.entities = [monster, self.player]

    def draw(self):
        # map
        for y in range(self.TILES_Y):
            for x in range(self.TILES_X):
                wall = self.map.tiles[x][y].blocked_sight
                if wall:
                    # self.con.draw_char(x, y, '#', fg=colors.gray_10, bg=colors.dark_wall)
                    self.con.draw_char(x, y, None, fg=None, bg=colors.dark_wall)
                else:
                    # self.con.draw_char(x, y, '.', fg=colors.gray_60, bg=colors.dark_ground)
                    self.con.draw_char(x, y, None, fg=None, bg=colors.dark_ground)

        render_entities(self.con, self.entities)
        # render_entity(self.con, self.player)

        # swap buffers
        render_blit(self.root_console, self.con, self.TILES_X, self.TILES_Y)

        # lazy, full clear.
        tdl.flush()
        render_clear_all(self.con, fg=colors.black, bg=colors.black)


    def input(self):
        pass

    def update(self):
        pass

    def loop(self):
        while not self.is_done and not tdl.event.is_window_closed():
            self.draw()

            # input
            for event in tdl.event.get():
                if event.type == 'KEYDOWN':
                    user_input = event
                    break
            else:
                user_input = None

            if not user_input:
                continue

            action = self.handle_input(user_input)
            move = action.get('move')
            exit = action.get('exit')
            fullscreen = action.get('fullscreen')

            if move:
                self.player.move(move[0], move[1])

            if exit:
                self.is_done = True

            if fullscreen:
                tdl.set_fullscreen(not tdl.get_fullscreen())

    def handle_input(self, user_input):
        # Movement keys
        if user_input.key == 'UP':
            return {'move': (0, -1)}
        elif user_input.key == 'DOWN':
            return {'move': (0, 1)}
        elif user_input.key == 'LEFT':
            return {'move': (-1, 0)}
        elif user_input.key == 'RIGHT':
            return {'move': (1, 0)}

        if user_input.key == 'ENTER' and user_input.alt:
            return {'fullscreen': True}
        elif user_input.key == 'ESCAPE':
            return {'exit': True}

        return {}


def random_font_path():
    font_dir = os.path.join(PATH_APP_ROOT, 'fonts')
    fonts = os.listdir(font_dir)
    path = os.path.join(font_dir, random.choice(fonts))
    print("Font: {}".format(path))
    return path


def main():
    g = Game()
    g.loop()


if __name__ == '__main__':
    # import tdl
    main()
    print('Done.')