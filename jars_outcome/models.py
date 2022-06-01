from django.db import models
from shared.models import BaseModel, SoftDeleteModel
# Create your models here.
from jars.models import Jar
from out_come.models import OutCome
from django.core.validators import MinValueValidator
class JarOutcome(BaseModel, SoftDeleteModel):
    jar = models.ForeignKey(
        Jar,
        on_delete=models.CASCADE,
        related_name='outcomes'
    )
    outcome = models.ForeignKey(
        OutCome,
        on_delete=models.CASCADE,
        related_name='jars'
    )
    price = models.DecimalField(
        max_digits=18, 
        decimal_places = 2,
        validators = [
            MinValueValidator(0.00)
        ],
        default = 0.00
    )