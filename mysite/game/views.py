from django.shortcuts import render, redirect
from game.models import Character, Monster
from django.template.loader import render_to_string


def home_view(request):
    if not (request.user.is_authenticated):
        return redirect("login")
    username = request.user.username
    return render(request, 'game/home.html', {'message': 'Logged in as: ' + username})


def character_view(request):
    if not (request.user.is_authenticated):
        return redirect("login")

    character = Character.objects.get(user=request.user)
    return render(request, 'game/character.html', {'name': character.name, 'maxHealth': character.maxHealth, 'currentHealth': character.currentHealth, 'damage': character.damage})


def fight_view(request):
    if not (request.user.is_authenticated):
        return redirect("login")

    monsters = Monster.objects.all()

    if(request.method == 'POST'):
        monster_id = request.POST['monster_id']
        monster = Monster.objects.get(id=monster_id)
        character = Character.objects.get(user=request.user)
        log = character.fight(monster)
        character.save()
        renderedLog = render_to_string('game/fightlog.html', {'message': log})
        return render(request, 'game/fight.html', {'monsters': monsters, 'log': renderedLog})

    return render(request, 'game/fight.html', {'monsters': monsters})


def healer_view(request):
    if not (request.user.is_authenticated):
        return redirect("login")

    if(request.method == 'POST'):
        character = Character.objects.get(user=request.user)
        message = character.heal()
        return render(request, 'game/healer.html', {'message': message})

    return render(request, 'game/healer.html')
