import pygame as pg
from pygame import mixer
from random import sample
import random
import sys
import os

WIDTH = 900
HEIGHT = 900
FPS = 60
LIVES = 3

WHITE = (45, 63, 70)
RED = (124, 41, 42)
GREEN = (0, 255, 0)
BLUE = (243, 164, 89)
BLACK = (200, 200, 200)
GRAY = (28, 40, 60)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Sudoku")
clock = pg.time.Clock()

key_to_number = {
            pg.K_0: 0, pg.K_1: 1, pg.K_2: 2, pg.K_3: 3,
            pg.K_4: 4, pg.K_5: 5, pg.K_6: 6, pg.K_7: 7,
            pg.K_8: 8, pg.K_9: 9,
        }