from enum import Enum, unique
import logging
import os
import random

import tdl # import tcod as libtcod

from app import colors
from app.render import (
    render_blit,
    render_clear_all,
    render_entities,
    random_font_path,
)

from app.map import Map, TileId

# logger = logging.getLogger(__name__)
logging.basicConfig(filename=os.path.join('logs','log.txt'), level=logging.DEBUG)

LIMIT_FPS = 60
PATH_APP_ROOT = os.path.dirname(os.path.abspath(__file__))

FOV_ALGO = 'BASIC'
FOV_LIGHT_WALL = True
USE_FOG_OF_WAR = False
TORCH_RADIUS = 10

@unique
class InputMode(Enum):
    GAME = 0
    EDITOR = 1


class Entity:
    def __init__(self, x, y, char, color, game):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.game = game
        self.map = game.map

    def move(self, dx, dy):
        if not self.map.is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

    def teleport_to(self, x, y):
        if self.map.in_bounds(x, y):
            self.x = x
            self.y = y


class Game:
    """
        see `init()`, definitions are not duplicated between it and `__init__()`
    members:
        root_console: main screen surface
        con: 2nd surface, back-buffer to render to root_console

    """
    def __init__(self):
        self.is_done = False
        self.TILES_X = 80
        self.TILES_Y = 50
        self.entities = []
        self.player = None
        self.map = Map(self.TILES_X, self.TILES_Y, self)
        self.map.debug_show_colors = True
        self.fov_recompute = True
        self.visible_tiles = [] # todo: move to map
        self.input_mode = InputMode.GAME

        self.init()
        path = os.path.join(PATH_APP_ROOT, 'fonts', 'arial12x12.png')
        tdl.set_font(path, greyscale=True, altLayout=True)
        self.root_console = tdl.init(self.TILES_X, self.TILES_Y, title='tcod demo', fullscreen=False)
        self.con = tdl.Console(self.TILES_X, self.TILES_Y)
        tdl.setFPS(LIMIT_FPS)
        logging.debug("FPS: {}".format(LIMIT_FPS))

    def re_init_font(self):
        # allows reloading of font
        path = random_font_path(PATH_APP_ROOT)
        logging.info("font: ", path)
        tdl.set_font(path, greyscale=True, altLayout=True)
        self.root_console = tdl.init(self.TILES_X, self.TILES_Y, title='tcod demo', fullscreen=False)
        self.con = tdl.Console(self.TILES_X, self.TILES_Y)
        tdl.setFPS(LIMIT_FPS)

    def init(self):
        # reset for next round, and first-time init.
        self.fov_recompute = True
        self.visible_tiles = []  # todo: move to map
        self.is_done = False
        self.TILES_X = 80
        self.TILES_Y = 50
        self.entities = []
        self.map.reset(self.TILES_X, self.TILES_Y)
        self.player = self.spawn("player")
        self.input_mode = InputMode.GAME

        self.map.gen_random_map()

    def spawn(self, name, **kwargs):
        if name == 'player':
            x = kwargs.get('x', 0)
            y = kwargs.get('y', 0)
            spawn = Entity(x, y, '@', colors.white, self)
            if self.player and self.player in self.entities:
                self.entities.remove(self.player)

            self.entities.append(spawn)
            self.player = spawn
            return spawn
        elif name == 'monster':
            x = kwargs.get('x', 0)
            y = kwargs.get('y', 0)
            char = str(kwargs.get('char','X'))
            spawn = Entity(x, y, char, colors.yellow, self)
            self.entities.append(spawn)
        elif name == 'debug':
            x = kwargs.get('x', 0)
            y = kwargs.get('y', 0)
            char = str(kwargs.get('char','X'))
            spawn = Entity(x, y, char, colors.black, self)
            self.entities.append(spawn)
        else:
            raise ValueError("Unknown spawn type: {}".format(name))

    def draw(self):
        # map
        for y in range(self.TILES_Y):
            for x in range(self.TILES_X):
                # check for both fog of war, and tile visibility/LOS

                tile_id = self.map.at(x, y).tile_id
                visible = (x, y) in self.visible_tiles
                explored = self.map.at(x, y).explored

                if not visible and not explored and USE_FOG_OF_WAR:
                    continue

                if visible and not explored:
                    self.map.at(x, y).explored = True

                if tile_id == TileId.WALL:
                    if visible:
                        color = colors.lit_dark_wall
                    else:
                        color = colors.dark_wall
                elif tile_id == TileId.FLOOR:
                    if visible:
                        color = colors.lit_dark_floor
                    else:
                        color = colors.dark_floor

                self.con.draw_char(x, y, None, fg=None, bg=color)


        render_entities(self.con, self.entities)

        # swap buffers
        render_blit(self.root_console, self.con, self.TILES_X, self.TILES_Y)

        # lazy, full clear.
        tdl.flush()
        render_clear_all(self.con, fg=colors.black, bg=colors.black)

    def input(self):
        for event in tdl.event.get():
            action = self.handle_input(event)

            if action:
                if action.get('move'):
                    self.player.move(*action.get('move'))

                if action.get('exit'):
                    self.is_done = True

                if action.get('fullscreen'):
                    tdl.set_fullscreen(not tdl.get_fullscreen())

    def update(self):
        if not self.fov_recompute:
            return

        # fov()
        self.fov_recompute = False
        self.visible_tiles = tdl.map.quickFOV(
            self.player.x,
            self.player.y,
            self.map.tile_is_visible,
            fov=FOV_ALGO,
            radius=TORCH_RADIUS,
            lightWalls=FOV_LIGHT_WALL
        )

    def loop(self):
        while not self.is_done and not tdl.event.is_window_closed():
            self.update()
            self.draw()
            self.input()

    def handle_input(self, event):
        # Movement keys
        if self.input_mode == InputMode.GAME:
            return self.handle_input_game(event)
        elif self.input_mode == InputMode.EDITOR:
            return self.handle_input_editor(event)
        else:
            raise Exception("Unknown game mode: {}".format(self.input_mode))

    def handle_input_game(self, event):
        RECOMPUTE_LOS_KEYS = ["UP", "DOWN", "LEFT", "RIGHT"]

        if event.type == 'KEYDOWN':
            # print(event)

            if event.key in RECOMPUTE_LOS_KEYS:
                self.fov_recompute = True

            # player
            if event.key == 'UP':
                return {'move': (0, -1)}
            elif event.key == 'DOWN':
                return {'move': (0, 1)}
            elif event.key == 'LEFT':
                return {'move': (-1, 0)}
            elif event.key == 'RIGHT':
                return {'move': (1, 0)}

            # debug / map / etc
            elif event.key == 'TAB':
                if self.input_mode == InputMode.GAME:
                    self.input_mode = InputMode.EDITOR
                else:
                    self.input_mode = InputMode.GAME
                print(self.input_mode)

            elif event.key == '1':
                self.map.room_gen_padding -= 1
                self.map.room_gen_padding = max(self.map.room_gen_padding, 0)
                logging.info("room padding: {}".format(self.map.room_gen_padding))
                self.init()
            elif event.key == '2':
                self.map.room_gen_padding += 1
                logging.info("room padding: {}".format(self.map.room_gen_padding))
                self.init()

            elif event.key == 'F1':
                self.map.debug_show_colors = not self.map.debug_show_colors
                self.init()
            elif event.key == 'PAGEUP':
                self.re_init_font()
            elif event.key == 'PAGEDOWN':
                self.re_init_font()

            elif event.key == 'SPACE':
                self.init()
            elif event.key == 'ESCAPE':
                return {'exit': True}
            elif event.key == 'ENTER' and event.alt:
                return {'fullscreen': True}

        # mice
        elif event.type == 'MOUSEDOWN':
            if event.button == 'LEFT':
                self.player.teleport_to(*event.cell)
                self.fov_recompute = True
                logging.info("Cell: {}".format(event.cell))

        return None

    def handle_input_editor(self, event):
        RECOMPUTE_LOS_KEYS = ["UP", "DOWN", "LEFT", "RIGHT"]

        if event.type == 'KEYDOWN':
            # print(event)

            if event.key in RECOMPUTE_LOS_KEYS:
                self.fov_recompute = True

            elif event.key == 'TAB':
                if self.input_mode == InputMode.GAME:
                    self.input_mode = InputMode.EDITOR
                else:
                    self.input_mode = InputMode.GAME
                print(self.input_mode)

            # player
            if event.key == 'UP':
                return {'move': (0, -1)}
            elif event.key == 'DOWN':
                return {'move': (0, 1)}
            elif event.key == 'LEFT':
                return {'move': (-1, 0)}
            elif event.key == 'RIGHT':
                return {'move': (1, 0)}

            elif event.key == 'SPACE':
                self.init()
            elif event.key == 'ESCAPE':
                return {'exit': True}

        # mice
        elif event.type == 'MOUSEDOWN':
            if event.button == 'LEFT':
                (x, y) = event.cell
                tile_id = self.map.at(x, y).tile_id
                if tile_id == TileId.WALL:
                    self.map.at(x, y).set_type(TileId.FLOOR)
                else:
                    self.map.at(x, y).set_type(TileId.WALL)
                self.fov_recompute = True

        return None



def main():
    g = Game()
    g.loop()


if __name__ == '__main__':
    print("""USE_FOG_OF_WAR = {}
TORCH_RADIUS = {}""".format(USE_FOG_OF_WAR, TORCH_RADIUS))
    main()
    print("To view hotkeys, see Game.handle_input")
    print('Done.')