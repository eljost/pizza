from collections import OrderedDict
from math import sqrt
import random
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
PIZZA_RADIUS = 450

# SALAMI
SALAMI_RADIUS = 35

topping_pngs = ("sauce.png", "salami.png", "cheese.png", "shroom.png", "brokooli.png")
TOPPINGS = [pg.image.load(png) for png in topping_pngs]


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
    return sqrt((w - pw) ** 2 + (h - ph) ** 2) <= PIZZA_RADIUS


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
    colors = [(i, i, i) for i in range(0, 200, 200 // len(topping_buttons))]
    menu_surf = pg.Surface((WIDTH, MENU_HEIGHT))
    for i, button in enumerate(topping_buttons):
        pg.draw.rect(menu_surf, colors[i], button)
        menu_surf.blit(TOPPINGS[i], (button.left, button.top))

    pizza = get_pizza()

    def draw():
        DISPLAY.blit(menu_surf, (0, 0))
        DISPLAY.blit(pizza, PIZZA_TOP_LEFT)

    cur_topping = 0

    def get_cur_png(rotate=False):
        cur_png = TOPPINGS[cur_topping].copy()
        if rotate:
            cur_png = pg.transform.rotate(cur_png, random.randrange(-180, 181))
        return cur_png
    cur_png = get_cur_png()

    draw()
    pg.display.update()
    while True:
        event = pg.event.wait()

        if event.type == pg.MOUSEBUTTONDOWN:
            pos = event.pos
            if on_menu(pos):
                mx, my = pg.mouse.get_pos()
                for i, button in enumerate(topping_buttons):
                    if button.collidepoint((mx, my)):
                        cur_topping = i
                        cur_png = get_cur_png(rotate=True)
                        print(f"Selected topping {i}")
            # Add topping if clicked on pizza
            p_pos = pizza_pos(pos)
            if on_pizza(p_pos):
                print("blit on pizza @", p_pos)
                pizza.blit(cur_png, p_pos)
                cur_png = get_cur_png(rotate=True)
            draw()
        elif event.type == pg.MOUSEMOTION:
            pos = event.pos
            draw()
            if not on_menu(pos):
                DISPLAY.blit(cur_png, pos)
        # Quit
        elif event.type == pg.QUIT:
            quit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                quit()

        pg.display.update()


main()
