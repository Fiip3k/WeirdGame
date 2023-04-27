from django.db import models
from django.conf import settings
# Create your models here.


class Fighter(models.Model):
    name = models.CharField(max_length=20)
    maxHealth = models.IntegerField()
    currentHealth = models.IntegerField()
    damage = models.IntegerField()
    isDead = models.BooleanField(default=False)

    def hit(self, opponent: 'Fighter') -> str:
        log = []

        # calculate damage
        damage = self.damage  # maybe armor, resists
        log.append(f"{self.name} hits {opponent.name} for {damage}.")

        # check if should kill or damage opponent
        if(opponent.currentHealth <= damage):
            log.append(f"{opponent.name} faints.")
            opponent.die()
        else:
            opponent.currentHealth -= damage

        return log

    def die(self) -> None:
        self.currentHealth = 0
        self.isDead = True

    def heal(self, target: 'Fighter' = None) -> list:
        log = []
        targetName = ''

        # if there was no target, heal self
        if target == None:
            target = self
            targetName = 'himself'
        else:
            targetName = target.name

        # if the target is alive and full health, don't heal
        if(target.currentHealth >= target.maxHealth and not target.isDead):
            return [f"{target.name} is fully healed."]

        # heal and revive character
        diff = target.maxHealth - target.currentHealth
        target.currentHealth = target.maxHealth
        target.isDead = False

        # log for how much the target was healed
        log += [f"{self.name} heals {targetName} for {diff} health."]

        target.save()
        return log


class Character(Fighter):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    strength = models.IntegerField(default=0)
    dexterity = models.IntegerField(default=0)
    intelligence = models.IntegerField(default=0)
    pointsToSpend = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    def fight(self, opponent: Fighter) -> tuple[list, bool]:
        # if self is dead, can't fight
        if (self.isDead):
            return (["You are dead."], False)
        log = []
        while(not self.isDead):
            # hit opponent
            log.extend(self.hit(opponent))

            # hit back if alive
            if(not opponent.isDead):
                log.extend(opponent.hit(self))
            else:
                break

        win = True
        if(self.isDead):
            win = False
        return (log, win)

    def increaseExperience(self, experience: int) -> None:
        startingExperience = 100
        experienceRequired = startingExperience * (1.5 ** (self.level - 1))
        self.experience += experience
        leveled = True
        while(leveled):
            if(self.experience >= experienceRequired):
                # level up
                self.level += 1
                self.pointsToSpend += 10
                experienceRequired = startingExperience * \
                    (1.5 ** (self.level - 1))
            else:
                leveled = False
        self.save()


class Monster(Fighter):
    experienceReward = models.IntegerField(default=0)
    goldReward = models.IntegerField(default=0)
