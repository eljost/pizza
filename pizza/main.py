import sys

import pygame as pg


SIZE = (1000, 1000)
WIDTH, HEIGHT = SIZE
CENTER = (WIDTH // 2, HEIGHT // 2)

# COLORS

WHITE = (255, 255, 255)
DOUGH = (255, 204, 153)
SALAMI = (165, 8, 8)

# DOUGH
RADIUS = 300

# SALAMI
SALAMI_RADIUS = 35

TOPPINGS = ("SAUCE", "CHEESE", "SALAMI", "MUSHROOMS", "TUNA")


def init(display):
    display.fill(WHITE)
    pg.draw.circle(display, DOUGH, CENTER, RADIUS)


def quit():
    pg.quit()
    sys.exit()


def main():
    pg.init()
    DISPLAY = pg.display.set_mode(SIZE)
    pg.mouse.set_visible(True)

    init(DISPLAY)
    pg.display.update()

    pos = CENTER
    pg.mouse.set_pos(pos)

    while True:
        event = pg.event.wait()

        # if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEMOTION:
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = event.pos
            pg.draw.circle(DISPLAY, SALAMI, pos, SALAMI_RADIUS)
            pg.display.update()
        elif event.type == pg.QUIT:
            quit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                quit()


main()
