import os
import random

# import tcod as libtcod
import tdl

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20
PATH_APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# root_console = None
# con = None  # back buffer
# isDone = False
# player_x, player_y = 1, 1


class Game:
    def __init__(self):
        self.init()
        # path = random_font_path()
        path = os.path.join(PATH_APP_ROOT, 'fonts', 'arial10x10.png')
        tdl.set_font(path, greyscale=True, altLayout=True)
        self.root_console = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title='tcod demo', fullscreen=False)
        self.con = tdl.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
        tdl.setFPS(LIMIT_FPS)

        self.isDone = False
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT // 2

    def init(self):
        self.isDone = False
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT // 2

    def draw(self):
        pass

    def input(self):
        pass

    def update(self):
        pass

    def loop(self):
        while not self.isDone and not tdl.event.is_window_closed():
            # draw
            self.con.draw_char(self.player_x, self.player_y, '@', bg=None, fg=(255, 255, 255))
            self.root_console.blit(self.con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)

            # swap buffers
            tdl.flush()

            # clear render
            self.con.draw_char(self.player_x, self.player_y, ' ', bg=None)

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
                dx, dy = move
                self.player_x += dx
                self.player_y += dy

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