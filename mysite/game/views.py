from django.shortcuts import render, redirect
from game.models import Character, Monster
from game.scripts.stats import Statistics, Statistic
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
            Statistics.increase(character, Statistic.Intelligence, intelligence)
            character.pointsToSpend -= total
            character.save()
        else:
            message['error'] = "Not enough points to spend."
            
    
    return render(request, 'game/character.html', message)


def fight_view(request):
    if not (request.user.is_authenticated):
        return redirect("login")

    monsters = Monster.objects.all()

    if(request.method == 'POST'):
        monster_id = request.POST['monster_id']
        monster = Monster.objects.get(id=monster_id)
        character = Character.objects.get(user=request.user)
        log, win = character.fight(monster)
        if(win):
            character.increaseExperience(monster.experienceReward)
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
