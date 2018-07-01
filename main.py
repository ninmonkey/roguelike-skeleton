import os
import random

# import tcod as libtcod
import tdl

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20
PATH_APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root_console = None


def random_font():
    font_dir = os.path.join(PATH_APP_ROOT, 'fonts')
    fonts = os.listdir(font_dir)
    path = os.path.join(font_dir, random.choice(fonts))
    libtcod.console_set_custom_font(path, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)


def init():
    global root_console
    #
    path = os.path.join(PATH_APP_ROOT, 'fonts', 'arial10x10.png')
    tdl.set_font(path, greyscale=True, altLayout=True)

    root_console = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title='tcod demo', fullscreen=False)
    tdl.setFPS(LIMIT_FPS)


def loop():
    global root_console

    while not tdl.event.is_window_closed():
        root_console.draw_char(1, 1, '@', bg=None, fg=(255,255,255))
        tdl.flush()


def main():
    init()
    loop()


if __name__ == '__main__':
    # import tdl
    main()
    print('Done.')