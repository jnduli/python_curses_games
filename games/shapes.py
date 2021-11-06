from collections import namedtuple
from dataclasses import dataclass
import abc
from typing import List
import curses

Point = namedtuple('Point', ['y', 'x'])

@dataclass()
class Character(abc.ABC):
    y: int
    x: int
    window: curses.window

    @abc.abstractmethod
    def body(self) -> List[tuple[int, int]]:
        """The body of the character"""

    @abc.abstractmethod
    def bounding_box(self) -> List[tuple[int, int]]:
        """The box the character is in"""

    def draw(self):
        for coord in self.body():
            self.window.addch(*coord, curses.ACS_CKBOARD)

    def clear(self):
        for coord in self.body():
            self.window.addch(*coord, ' ')

    @abc.abstractmethod
    def move(self):
        """How the character moves in every tick, just update the x and y"""
