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


class Entity:
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self,  dx, dy):
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
        self.root_console = tdl.init(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, title='tcod demo', fullscreen=False)
        self.con = tdl.Console(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        tdl.setFPS(LIMIT_FPS)

    def init(self):
        # reset for next round
        self.isDone = False
        self.SCREEN_WIDTH = 80
        self.SCREEN_HEIGHT = 50

        player_x = self.SCREEN_WIDTH // 2
        player_y = self.SCREEN_HEIGHT // 2
        self.player = Entity(player_x, player_y, '@', colors.white)

        monster = Entity(self.player.x - 2, self.player.y, '@', colors.yellow)
        self.entities = [monster, self.player]

    def draw(self):
        render_entities(self.con, self.entities)
        # render_entity(self.con, self.player)

        # swap buffers
        render_blit(self.root_console, self.con, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        # lazy, full clear.
        tdl.flush()
        render_clear_all(self.con, fg=colors.black, bg=colors.black)


    def input(self):
        pass

    def update(self):
        pass

    def loop(self):
        while not self.isDone and not tdl.event.is_window_closed():
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
                self.isDone = True

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