from django.db import models
from shared.models import BaseModel, SoftDeleteModel
from in_come.models import Income
from wallet.models import Wallet
from django.core.validators import MinValueValidator
# Create your models here.
class IncomeWallet(BaseModel,SoftDeleteModel):
    income = models.ForeignKey(
        Income,
        on_delete=models.CASCADE,
        related_name= 'wallets'
    )
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name= 'incomes'
    )
    price = models.DecimalField(
        max_digits=18, 
        decimal_places = 2,
        validators = [
            MinValueValidator(0.00)
        ],
        default = 0.00
    )