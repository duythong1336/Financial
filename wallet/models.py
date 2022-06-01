from tkinter import CASCADE
from django.db import models
from shared.models import BaseModel, SoftDeleteModel
from django.core.validators import MinValueValidator
from user.models import User
# Create your models here.
class Wallet(BaseModel, SoftDeleteModel):
    name = models.CharField(max_length= 255, default="")
    description = models.CharField(max_length=255, default="")
    price = models.DecimalField(
        max_digits=18, 
        decimal_places = 2,
        validators = [
            MinValueValidator(0.00)
        ],
        default = 0.00
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name= 'wallets'
    )