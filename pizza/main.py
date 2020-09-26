from collections import OrderedDict
from math import sqrt
import sys

import numpy as np
import pygame as pg


SIZE = (1000, 1000)
WIDTH, HEIGHT = SIZE
MENU_HEIGHT = 100
PIZZA_SIZE = (WIDTH, HEIGHT - MENU_HEIGHT)
PIZZA_WIDTH, PIZZA_HEIGHT = PIZZA_SIZE
PIZZA_CENTER = (PIZZA_WIDTH // 2, PIZZA_HEIGHT // 2)
PIZZA_TOP_LEFT = (0, MENU_HEIGHT)

# COLORS

C_WHITE = (255, 255, 255)
C_DOUGH = (255, 204, 153)
C_SAUCE = (255, 0, 0)
C_CHEESE = (255, 255, 0)
C_SALAMI = (165, 8, 8)

# PIZZA
PIZZA_RADIUS = 300

# SALAMI
SALAMI_RADIUS = 35

TOPPINGS = ("SAUCE", "CHEESE", "SALAMI")
TOPPING_DICT = {
    "SAUCE": C_SAUCE,
    "CHEESE": C_CHEESE,
    "SALAMI": C_SALAMI,
}


def get_pizza():
    pizza = pg.Surface(PIZZA_SIZE)
    pizza.fill(C_WHITE)
    pg.draw.circle(pizza, C_DOUGH, PIZZA_CENTER, PIZZA_RADIUS)
    return pizza


def on_menu(pos):
    w, h = pos
    return h <= MENU_HEIGHT


def on_pizza(pos):
    w, h = pos
    pw, ph = PIZZA_CENTER
    return sqrt((w-pw)**2 + (h-ph)**2) <= PIZZA_RADIUS


def pizza_pos(pos):
    return (pos[0], pos[1] - MENU_HEIGHT)


def get_topping_buttons(num=None):
    """See also https://stackoverflow.com/a/47664205"""
    if num is None:
        num = len(TOPPINGS)
    width = WIDTH // num
    left = 0
    top = 0
    buttons = list()
    for i in range(num):
        buttons.append(pg.Rect(left, top, width, MENU_HEIGHT))
        left += width
    return buttons


def quit():
    pg.quit()
    sys.exit()


def main():
    pg.init()
    DISPLAY = pg.display.set_mode(SIZE)

    # Mouse
    pg.mouse.set_visible(True)
    pos = PIZZA_CENTER
    pg.mouse.set_pos(pos)

    # Setup topping buttons
    topping_buttons = get_topping_buttons()
    colors = [(i, i, i) for i in range(0, 200, 200//len(topping_buttons))]
    menu_surf = pg.Surface((WIDTH, MENU_HEIGHT))
    for i, button in enumerate(topping_buttons):
        pg.draw.rect(menu_surf, colors[i], button)

    pizza = get_pizza()

    def draw():
        DISPLAY.blit(menu_surf, (0, 0))
        DISPLAY.blit(pizza, PIZZA_TOP_LEFT)


    cur_topping = 0
    cur_color = TOPPING_DICT[TOPPINGS[cur_topping]]
    draw()
    pg.display.update()
    while True:
        event = pg.event.wait()
        mx, my = pg.mouse.get_pos()


        if event.type == pg.MOUSEBUTTONDOWN:
            pos = event.pos
            if on_menu(pos):
                for i, button in enumerate(topping_buttons):
                    if button.collidepoint((mx, my)):
                        cur_topping = i
                        print(f"Selected topping {i}")
            p_pos = pizza_pos(pos)
            if on_pizza(p_pos):
                pg.draw.circle(pizza, C_SALAMI, p_pos, SALAMI_RADIUS)
            draw()
        elif event.type == pg.MOUSEMOTION:
            pos = event.pos
            draw()
            if not on_menu(pos):
                pg.draw.circle(DISPLAY, C_SALAMI, pos, SALAMI_RADIUS)
        # Quit
        elif event.type == pg.QUIT:
            quit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                quit()

        pg.display.update()


main()
