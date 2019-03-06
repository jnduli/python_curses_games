from curses import wrapper
from .tetris import Tetris

def tetris(stdscreen):
    tetris = Tetris(stdscreen)
    tetris.loop()

if __name__ == '__main__':
    wrapper(tetris)

