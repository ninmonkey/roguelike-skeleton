import os
import random

import tcod as libtcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20
PATH_APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def random_font():
    font_dir = os.path.join(PATH_APP_ROOT, 'fonts')
    fonts = os.listdir(font_dir)
    path = os.path.join(font_dir, random.choice(fonts))
    libtcod.console_set_custom_font(path, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)


def init():
    path = os.path.join(PATH_APP_ROOT, 'fonts', 'arial10x10.png')
    # random_font()
    libtcod.console_set_custom_font(path, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'libtcod tutorial revised', False)

    # if real time
    # libtcod.sys_set_fps(LIMIT_FPS)


def loop():
    while not libtcod.console_is_window_closed():
        libtcod.console_set_default_foreground(0, libtcod.white)
        libtcod.console_put_char(0, 1, 1, '@', libtcod.BKGND_NONE)
        libtcod.console_flush()

        key = libtcod.console_check_for_keypress()

        if key.vk == libtcod.KEY_ESCAPE:
            return True


def main():
    init()
    loop()


if __name__ == '__main__':
    main()
    print('Done.')