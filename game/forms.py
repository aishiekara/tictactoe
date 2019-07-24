import random
import re

from django import forms
from django.core.exceptions import ImproperlyConfigured, ValidationError

from .players import get_player
from .models import Game


def validate_player_type(player_type):
    if player_type.strip() != '':
        return True
    try:
        return get_player(player_type) is not None
    except (ImproperlyConfigured, ImportError):
        raise ValidationError("Unknown player type: " + player_type)


class NewGameForm(forms.Form):
    player1 = forms.CharField(max_length=64, required=True,
                              validators=[validate_player_type])
    player2 = forms.CharField(max_length=64, required=True,
                              validators=[validate_player_type])
    def create(self):
        "Creates a game."
        players = [self.cleaned_data['player1'], self.cleaned_data['player2']]
        random.shuffle(players)
        game = Game()
        game.player_x = players[0]
        game.player_o = players[1]
        return game

class PlayForm(forms.Form):
    index = forms.IntegerField(min_value=0, max_value=8)
