from django.db import models
from django.conf import settings
# Create your models here.


class Character(models.Model):
    name = models.CharField(max_length=20)
    max_health = models.IntegerField()
    current_health = models.IntegerField()
    damage = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
