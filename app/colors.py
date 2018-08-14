from tcod import Color

from random import randint

"""

# todo: rewrite as dict or at least refactor to be internally-consistent

see also:
    - https://python-tdl.readthedocs.io/en/latest/libtcodpy.html#tcod.color_gen_map
    - https://python-tdl.readthedocs.io/en/latest/libtcodpy.html#color
"""


def color_step(original, step):
    return Color(*original) + Color(step, step, step)


def gen_gray_percent(fraction, base):
    r = int(fraction * base)
    g = int(fraction * base)
    b = int(fraction * base)
    return r, g, b


def random_color():
    return randint(0, 255), randint(0, 255), randint(0, 255)


def random_hue():
    raise NotImplementedError('wip HSL randomized color around a hue')


yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
red_dark = (80, 0, 0)
green = (0, 255, 0)
dark_green = (60, 140, 60)

desaturated_green = (63, 127, 63)
darker_green = (0, 127, 0)
light_amber = (255, 219, 114)
sepia = (127, 101, 63)

gray_0 = black
gray_10 = gen_gray_percent(0.1, 255)
gray_20 = gen_gray_percent(0.2, 255)
gray_30 = gen_gray_percent(0.3, 255)
gray_40 = gen_gray_percent(0.4, 255)
gray_50 = gen_gray_percent(0.5, 255)
gray_60 = gen_gray_percent(0.6, 255)
gray_70 = gen_gray_percent(0.7, 255)
gray_80 = gen_gray_percent(0.8, 255)
gray_90 = gen_gray_percent(0.9, 255)
gray_100 = white

# dynamic
step_10 = int((255/10)*2)
step_20 = int((255/10)*2)
step_30 = int((255/10)*2)
step_40 = int((255/10)*2)

# aliases

dark_wall = gray_20
dark_floor = gray_50

lit_dark_wall = color_step(dark_wall, step_20)
lit_dark_floor = color_step(dark_floor, step_20)

orc = desaturated_green
troll = light_amber
rat = sepia
