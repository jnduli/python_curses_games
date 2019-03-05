from curses import wrapper
from .tetris import tetris

if __name__ == '__main__':
    wrapper(tetris)

