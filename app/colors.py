from random import randint

# todo: rewrite as dict Or at least refactor to be internally-consistent


def gen_gray_percent(fraction, base):
    r = int(fraction * base)
    g = int(fraction * base)
    b = int(fraction * base)
    return r, g, b


def random_color():
    return randint(0, 255), randint(0, 255), randint(0, 255)


def random_hue():
    raise NotImplementedError('wip HSL randomized color')

# def gen_color_percent(color1, percent_r, percent_g, percent_b):
#     r = int(color1[0] * percent_r)
#     g = int(color1[1] * percent_g)
#     b = int(color1[2] * percent_b)
#     return r, g, b


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

dark_wall = gray_20
dark_floor = gray_50

lit_dark_wall = gray_40
lit_dark_floor = gray_70

orc = desaturated_green
troll = light_amber
rat = sepia
