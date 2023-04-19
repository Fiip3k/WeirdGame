from enum import Enum
from game.models import Character


class Statistic(Enum):
    Strength = 1
    Dexterity = 2
    Intelligence = 3


class Statistics(object):
    def increase(character: 'Character', statistic: Statistic, amount: int = 1):
        match statistic:
            case Statistic.Strength:
                character.strength += amount
                character.maxHealth += amount*10
                character.currentHealth += amount*10
                character.damage += amount*5
            case Statistic.Dexterity:
                character.dexterity += amount
                character.damage += amount*10
            case Statistic.Intelligence:
                character.intelligence += amount
                character.maxHealth += amount*5
                character.currentHealth += amount*5
                character.damage += amount*5
