from curses import wrapper
from .tetris import Tetris
import logging

logging.basicConfig(filename='tetris.log',level=logging.INFO)

def tetris(stdscreen):
    tetris = Tetris(stdscreen)
    tetris.loop()

if __name__ == '__main__':
    wrapper(tetris)

