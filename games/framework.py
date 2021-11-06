import abc

class Game(abc.ABC):

    @abc.abstractmethod
    def create_score_window(self):
        """ Window that shows the scores """

    @abc.abstractmethod
    def create_game_window(self):
        """ Active game window """

    @abc.abstractmethod
    def update_score(self):
        """ Updates the score window """

    @abc.abstractmethod
    def loop(self):
        """ Main game loop """
