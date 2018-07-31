import os
import random
from app import colors


# todo: better rename funcs now that they are under namespace

def random_font_path(path_app_root):
    font_dir = os.path.join(path_app_root, 'fonts')
    fonts = [x for x in os.listdir(font_dir) if not os.path.isdir(x)]
    path = os.path.join(font_dir, random.choice(fonts))
    return path


def render_blit(root_con, con, width, height):
    root_con.blit(con, 0, 0, width, height, 0, 0)


def render_entity(con, entity):
    con.draw_char(entity.x, entity.y, entity.char, bg=None, fg=entity.color)


def render_entities(con, entities):
    for entity in entities:
        render_entity(con, entity)


def render_clear_all(con, fg=None, bg=None):
    if fg is None:
        fg = colors.black
    if bg is None:
        bg = colors.black
    con.clear(fg, bg)


def clear_entity(con, entity):
    con.draw_char(entity.x, entity.y, ' ', bg=None, fg=entity.color)


def clear_all_entities(con, entities):
    for entity in entities:
        clear_entity(entity)
