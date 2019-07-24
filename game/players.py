"""
Players are defined their "play" method, which takes a game model
They are expected to return an index that is their play.
"""
import random
from django.utils.module_loading import import_string


class RandomPlayer(object):
    """
    The random player plays in a random square. It's not very smart.
    """

    def play(self, game):
        # Find a spot on the board that's open.
        open_indexes = [i for i, v in enumerate(game.board) if v == ' ']
        if not open_indexes:
            return
        return random.choice(open_indexes)


def get_player(player_type):
    cls = import_string(player_type)
    return cls()
