from settings import *
from resources import *

pg.init()

font_numbers = pg.font.SysFont(None, 45)
font_title = pg.font.SysFont(None, 80)

def main():
    while True:
        grid = Grid()
        player = Player(grid)
        player.round(grid)

if __name__ == "__main__":
    main()