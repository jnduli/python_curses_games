from .race import Race
from curses import wrapper


def racing(stdscreen):
    race = Race(stdscreen)
    race.loop()


if __name__ == '__main__':
    wrapper(racing)
