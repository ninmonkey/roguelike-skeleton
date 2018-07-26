from app import colors


# todo: better rename funcs now that they are under namespace

def random_font_path():
    font_dir = os.path.join(PATH_APP_ROOT, 'fonts')
    fonts = os.listdir(font_dir)
    path = os.path.join(font_dir, random.choice(fonts))
    print("Font: {}".format(path))
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
