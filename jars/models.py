from django.db import models
from user.models import User
from shared.models import BaseModel, SoftDeleteModel
# Create your models here.

class JarChoice(models.TextChoices):
    NEC = "NEC"
    FFA = "FFA"
    LTSS = "LTSS"
    EDU = "EDU"
    PLAY = "PLAY"
    GIVEN = "GIVEN"

class Jar(BaseModel, SoftDeleteModel):
    name = models.CharField(
        max_length=10,
        choices=JarChoice.choices,
        default = ""
    )
    percent = models.IntegerField(default = 0)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name=  'jars'
    )
