import os
import random

# import tcod as libtcod
import tdl

from app import colors

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
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
    def __init__(self):
        self.init()
        # path = random_font_path()
        path = os.path.join(PATH_APP_ROOT, 'fonts', 'arial10x10.png')
        tdl.set_font(path, greyscale=True, altLayout=True)
        self.root_console = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title='tcod demo', fullscreen=False)
        self.con = tdl.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
        tdl.setFPS(LIMIT_FPS)

    def init(self):
        # reset for next round
        self.isDone = False

        monster = Entity(38, 24, '@', colors.yellow)
        self.entities = [monster]

        player_x = SCREEN_WIDTH // 2
        player_y = SCREEN_HEIGHT // 2
        self.player = Entity(player_x, player_y, '@', colors.white)

    def draw(self):
        # draw

        for entity in self.entities:
            self.con.draw_char(entity.x, entity.y, entity.char, bg=None, fg=entity.color)

        self.con.draw_char(self.player.x, self.player.y, self.player.char, bg=None, fg=self.player.color)

        # swap buffers
        self.root_console.blit(self.con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
        tdl.flush()

        # clear render: full clear vs dirty blits
        self.con.clear(fg=colors.black, bg=colors.black)
        # else:
        #     self.con.draw_char(self.player.x, self.player.y, ' ', bg=None)
        #     for entity in self.entities:
        #         self.con.draw_char(entity.x, entity.y, ' ', bg=None, fg=entity.color)


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