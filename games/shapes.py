from collections import namedtuple
from dataclasses import dataclass
from ABC import abstractmethod
from typing import List
import curses

Point = namedtuple('Point', ['y', 'x'])

@dataclass()
class Character:
    y: int
    x: int
    window: curses.window

    @abstractmethod()
    def body(self) -> List[tuple[int, int]]:
        """The body of the character"""

    @abstractmethod()
    def bounding_box(self) -> List[tuple[int, int]]:
        """The box the character is in"""

    def draw(self):
        for coord in self.body():
            self.window.addch(*coord, curses.ACS_CKBOARD)

    def clear(self):
        for coord in self.body():
            self.window.addch(*coord, ' ')

    @abstractmethod()
    def move(self):
        """How the character moves in every tick, just update the x and y"""
