from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .forms import NewGameForm, PlayForm
from .models import Game

@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == "POST":
        form = NewGameForm(request.POST)
        if form.is_valid():
            game = form.create()
            ret = game.save()
            return redirect(game)
    else:
        form = NewGameForm()

    # get players scores
    players = getScores()
    return render(request, 'game/game_list.html', {'form': form, 'players': players})

@require_http_methods(["GET", "POST"])
def game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == "POST":
        # Check for index.
        form = PlayForm(request.POST)
        if form.is_valid():
            game.play(form.cleaned_data['index'])
            game.save()
            return redirect(game)
        else:
            pass

    return render(request, "game/game_detail.html", {
        'game': game
    })


def getScores():

    latest_games = Game.objects.all()
    players = {}
    for i in latest_games:
        if i.winner and i.winner in players:
            players[i.winner]['score'] += 1
        elif i.winner:
            players[i.winner] = {'name': i.winner, 'score': 1}

    sortedplayers = sorted(players.values(), key=lambda kv: kv['score'], reverse=True)
    print(sortedplayers)
    return sortedplayers
    
