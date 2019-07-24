"""tictactoe URL Configuration"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('game/', include(('game.urls', 'game'), namespace='game')),
    path('admin/', admin.site.urls),
]
