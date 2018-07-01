import os
import random

# import tcod as libtcod
import tdl

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20
PATH_APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root_console = None
con = None  # back buffer
isDone = False
player_x, player_y = 1, 1


# def random_font():
#     font_dir = os.path.join(PATH_APP_ROOT, 'fonts')
#     fonts = os.listdir(font_dir)
#     path = os.path.join(font_dir, random.choice(fonts))
#     libtcod.console_set_custom_font(path, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)


def init():
    global root_console, con
    global player_x, player_y

    # entities
    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT // 2

    # render
    path = os.path.join(PATH_APP_ROOT, 'fonts', 'arial10x10.png')
    tdl.set_font(path, greyscale=True, altLayout=True)
    root_console = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title='tcod demo', fullscreen=False)
    con = tdl.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
    tdl.setFPS(LIMIT_FPS)


def loop():
    global root_console, con
    global player_x, player_y
    global isDone

    while not isDone and not tdl.event.is_window_closed():
        # draw
        con.draw_char(player_x, player_y, '@', bg=None, fg=(255, 255, 255))
        root_console.blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
        tdl.flush()

        # clear buffer?
        con.draw_char(player_x, player_y, ' ', bg=None)

        # input
        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
        else:
            user_input = None

        if not user_input:
            continue

        action = handle_input(user_input)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            player_x += dx
            player_y += dy

        if exit:
            isDone = True

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())


def handle_input(user_input):
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
    init()
    loop()


if __name__ == '__main__':
    # import tdl
    main()
    print('Done.')