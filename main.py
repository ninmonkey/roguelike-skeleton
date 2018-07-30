import os
import random

import tdl # import tcod as libtcod

from app import colors
from app.render import (
    render_blit,
    render_clear_all,
    render_entities,
)

from app.map import Map

LIMIT_FPS = 20
PATH_APP_ROOT = os.path.dirname(os.path.abspath(__file__))


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
        self.init()
        # path = random_font_path()
        path = os.path.join(PATH_APP_ROOT, 'fonts', 'arial10x10.png')
        tdl.set_font(path, greyscale=True, altLayout=True)
        self.root_console = tdl.init(self.TILES_X, self.TILES_Y, title='tcod demo', fullscreen=False)
        self.con = tdl.Console(self.TILES_X, self.TILES_Y)
        tdl.setFPS(LIMIT_FPS)

    def init(self):
        # reset for next round, and first-time init.
        self.is_done = False
        self.TILES_X = 80
        self.TILES_Y = 50
        self.entities = []
        self.player = None
        self.map = Map(self.TILES_X, self.TILES_Y, self)
        self.player = self.spawn("player")

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
            spawn = Entity(x, y, 'X', colors.yellow, self)
            self.entities.append(spawn)
        else:
            raise ValueError("Unknown spawn type: {}".format(name))

    # def add_entity(self, entity):
    #     self.entities.append(entity)

    def draw(self):
        # map
        for y in range(self.TILES_Y):
            for x in range(self.TILES_X):
                color = self.map.at(x, y).color
                self.con.draw_char(x, y, None, fg=None, bg=color)

        render_entities(self.con, self.entities)

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

            # todo: (verify) but I think this consumes only one event per loop
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

            if action.get('move'):
                self.player.move(*action.get('move'))

            if action.get('exit'):
                self.is_done = True

            if action.get('fullscreen'):
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


def main():
    g = Game()
    g.loop()


if __name__ == '__main__':
    main()
    print('Done.')