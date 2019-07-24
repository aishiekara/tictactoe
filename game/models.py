from collections import Counter
from django.db import models
from django.urls import reverse

class Game(models.Model):
    """
    This defines the board for a tic-tac-toe game.
    The board cells is represented with numbers 1-9:
    	'X' or 'O' means the cell is played.
    """
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    board = models.CharField(max_length=9, default=" "*9)

    player_x = models.CharField(max_length=64)
    player_o = models.CharField(max_length=64)
    winner = models.CharField(max_length=64, default='')

    WINNING = [
        [0, 1, 2],  # Across top
        [3, 4, 5],  # Across middle
        [6, 7, 8],  # Across bottom
        [0, 3, 6],  # Down left
        [1, 4, 7],  # Down middle
        [2, 5, 8],  # Down right
        [0, 4, 8],  # Diagonal ltr
        [2, 4, 6],  # Diagonal rtl
    ]

    def __unicode__(self):
        return '{0} vs {1}, state="{2}"'.format(self.player_x, self.player_o, self.board)

    def get_absolute_url(self):
        return reverse('game:detail', kwargs={'pk': self.pk})

    @property
    def next_player(self):
        # Counter is a useful class that counts objects.
        count = Counter(self.board)
        if count.get('X', 0) > count.get('O', 0):
            return 'O'
        return 'X'

    @property
    def is_game_over(self):
        """
        If the game is over and there is a winner, returns 'X' or 'O'.
        If the game is a stalemate, it returns ' ' (space)
        If the game isn't over, it returns None.
        """
        board = list(self.board)
        for wins in self.WINNING:
            # Create a tuple
            w = (board[wins[0]], board[wins[1]], board[wins[2]])
            if w == ('X', 'X', 'X'):
                self.winner = self.player_x
                self.save()
                return 'X'
            if w == ('O', 'O', 'O'):
                self.winner = self.player_o
                self.save()
                return 'O'
        # Check for stalemate
        if ' ' in board:
            return None
        return ' '

    def play(self, index):
        """
        Plays a square specified by index.
        The player to play is implied by the board state.

        If the play is invalid, it raises a ValueError.
        """
        if index < 0 or index >= 9:
            raise IndexError("Invalid board index")

        if self.board[index] != ' ':
            raise ValueError("Square already played")

        board = list(self.board)
        board[index] = self.next_player
        self.board = u''.join(board)

    def play_auto(self):
        """Plays for any artificial/computers players.
        Returns when the computer players have played or the game is over."""
        from .players import get_player

        while not self.is_game_over:
            next = self.next_player
            player = self.player_x if next == 'X' else self.player_o
            if player != '':
                return

            player_obj = get_player(player)
            self.play(player_obj.play(self))
