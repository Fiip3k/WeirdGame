from django.shortcuts import render, redirect
from game.models import Character


def home_view(request):
    if not (request.user.is_authenticated):
        return redirect("login")
    username = request.user.username
    return render(request, 'game/home.html', {'message': 'Logged in as: ' + username})


def character_view(request):
    character = Character.objects.get(user=request.user)
    return render(request, 'game/character.html', {'name': character.name, 'max_health': character.max_health, 'current_health': character.current_health, 'damage': character.damage})
