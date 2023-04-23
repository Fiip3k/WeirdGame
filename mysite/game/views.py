from django.shortcuts import render, redirect
from game.models import Character, Monster
from game.scripts.stats import Statistics, Statistic
from django.template.loader import render_to_string


def home_view(request):
    if not (request.user.is_authenticated):
        return redirect("login")

    character = Character.objects.get(user=request.user)
    message = dict()
    message['character'] = character
    message['message'] = 'Logged in as: ' + request.user.username

    return render(request, 'game/home.html', message)


def character_view(request):
    if not (request.user.is_authenticated):
        return redirect("login")

    character = Character.objects.get(user=request.user)
    message = dict()
    message['character'] = character

    if(request.method == 'POST'):
        strength = int(request.POST['strengthIncrease'])
        dexterity = int(request.POST['dexterityIncrease'])
        intelligence = int(request.POST['intelligenceIncrease'])
        total = strength + dexterity + intelligence
        if(character.pointsToSpend >= total):
            Statistics.increase(character, Statistic.Strength, strength)
            Statistics.increase(character, Statistic.Dexterity, dexterity)
            Statistics.increase(
                character, Statistic.Intelligence, intelligence)
            character.pointsToSpend -= total
            character.save()
        else:
            message['error'] = "Not enough points to spend."

    return render(request, 'game/character.html', message)


def fight_view(request):
    if not (request.user.is_authenticated):
        return redirect("login")

    character = Character.objects.get(user=request.user)
    message = dict()
    message['monsters'] = Monster.objects.all()  # TODO

    for monster in message['monsters']:
        monster.currentHealth *= character.level
        monster.maxHealth *= character.level
        monster.damage *= character.level

    if(request.method == 'POST'):
        monster_id = int(request.POST['monster_id'])
        target = [m for m in message['monsters'] if m.id == monster_id]
        log, win = character.fight(target[0])
        if(win):
            character.increaseExperience(monster.experienceReward)
        character.save()
        message['character'] = character
        message['log'] = render_to_string(
            'game/fightlog.html', {'message': log})
        return render(request, 'game/fight.html', message)
    message['character'] = character
    return render(request, 'game/fight.html', message)


def healer_view(request):
    if not (request.user.is_authenticated):
        return redirect("login")

    character = Character.objects.get(user=request.user)
    message = dict()
    message['character'] = character

    if(request.method == 'POST'):
        character = Character.objects.get(user=request.user)
        message['message'] = character.heal()
        message['character'] = character
        return render(request, 'game/healer.html', message)

    return render(request, 'game/healer.html', message)
