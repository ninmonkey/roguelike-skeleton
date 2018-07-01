import os
import random

# import tcod as libtcod
import tdl

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20
PATH_APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root_console = None
isDone = False
player_x, player_y = 1, 1


def random_font():
    font_dir = os.path.join(PATH_APP_ROOT, 'fonts')
    fonts = os.listdir(font_dir)
    path = os.path.join(font_dir, random.choice(fonts))
    libtcod.console_set_custom_font(path, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)


def init():
    global root_console
    global player_x, player_y
    
    # entities
    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT // 2

    # render
    path = os.path.join(PATH_APP_ROOT, 'fonts', 'arial10x10.png')
    tdl.set_font(path, greyscale=True, altLayout=True)

    root_console = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title='tcod demo', fullscreen=False)
    tdl.setFPS(LIMIT_FPS)


def loop():
    global root_console
    global player_x, player_y

    while not isDone and not tdl.event.is_window_closed():
        root_console.draw_char(player_x, player_y, '@', bg=None, fg=(255, 255, 255))
        tdl.flush()

        handle_input()


# def handle_input_realtime():
#
#     keypress = False
#     for event in tdl.event.get():
#         if event.type == 'KEYDOWN':
#             user_input = event
#             keypress = True
#     if not keypress:
#         return


def handle_input():
    global isDone
    global player_x, player_y

    user_input = tdl.event.key_wait()

    if user_input.key == 'ENTER' and user_input.alt:
        tdl.set_fullscreen(not tdl.get_fullscreen())

    elif user_input.key == 'ESCAPE':
        isDone = True
        return

    if user_input.key == 'UP':
        player_y -= 1
    elif user_input.key == 'DOWN':
        player_y += 1
    elif user_input.key == 'LEFT':
        player_x -= 1
    elif user_input.key == 'RIGHT':
        player_x += 1




def main():
    init()
    loop()


if __name__ == '__main__':
    # import tdl
    main()
    print('Done.')