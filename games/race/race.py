import curses
from .car import Car
from .villains import Villains
from .collisions import Collision

class Race(Collision):
    def __init__(self, stdscreen):
        curses.curs_set(0)
        self.game_window = self.create_game_board(stdscreen)
        height, width = self.game_window.getmaxyx()
        self.score_window = self.create_score_board(stdscreen)
        self.hero = Car(y=(height*3)//5, x=width//3 + 1)
        self.left_limit = 1 
        self.right_limit = width - 4
        self.villains = Villains() 
        key = 0
        self.score = 0

    def loop(self):
        key = 0
        score = 0
        while key is not ord('q'):
            key = self.game_window.getch()
            self.villains.random_add(self.hero)
            self.hero.draw(self.game_window)
            self.villains.move(self.game_window)
            self.villains.draw(self.game_window)
            new_x = self.hero_motion(key) * 4 + self.hero.x
            if new_x < self.left_limit:
                new_x = self.left_limit
            if new_x > self.right_limit:
                new_x = self.right_limit
            if self.hero.x is not new_x:
                self.hero.move(self.game_window, y=self.hero.y, x = new_x)
            if (self.check_for_collisions(self.hero, self.villains)):
                return
            before_clear = len(self.villains)
            self.villains.remove(self.game_window)
            after_clear = len(self.villains)
            score = score + (before_clear - after_clear )
            self.updateScore(self.score_window, score)

    def create_game_board(self, stdscreen):
        height, width = stdscreen.getmaxyx()
        window = curses.newwin(height, 13, 0 , width//2)
        window.keypad(1)
        window.timeout(100)
        window.border(0,0,0,0,0,0,0,0)
        return window

    def create_score_board(self, stdscreen):
        height, width = stdscreen.getmaxyx()
        window = curses.newwin(height, width//2 - 20, 0 , width//2 + 14)
        window.border(0,0,0,0,0,0,0,0)
        window.addstr(height//4, 1, 'Press q to leave racing game')
        window.refresh()
        return window

    def hero_motion(self, key):
        if key in [curses.KEY_LEFT, ord('h')]:
            return -1
        elif key in [curses.KEY_RIGHT, ord('l')]:
            return 1
        else:
            return 0

    def updateScore(self, scoreWindow, score):
        scoreMessage = 'Score: {}'.format(score)
        height, width = scoreWindow.getmaxyx()
        scoreWindow.addstr(height//2, width//2, scoreMessage)
        scoreWindow.refresh()
