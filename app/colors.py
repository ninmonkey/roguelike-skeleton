# todo: rewrite as dict Or at least refactor to be internally-consistent

def gen_gray_percent(fraction, base):
    r = int(fraction * base)
    g = int(fraction * base)
    b = int(fraction * base)
    return r, g, b


yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
red_dark = (80, 0, 0)

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

