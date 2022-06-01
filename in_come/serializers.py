
from rest_framework import serializers,exceptions
from in_come.models import Income
from django.core.validators import MinValueValidator
from wallet.models import Wallet
from income_wallet.models import IncomeWallet
class InComeItemSerializer(serializers.Serializer):
    name = serializers.CharField(required = True)
    description = serializers.CharField(required = True)
    price = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators = [
            MinValueValidator(0.00)
        ],
        required = True
    ) 
    class Meta:
        fields = ['name', 'description', 'price']
        
class CreateIncomeSerializer(serializers.Serializer):
    items = serializers.ListField(
        child = InComeItemSerializer()
    )
    def save(self):
        incomes = []
        items = self.validated_data['items']
        for item in items:
            income = Income(
                name = item.get('name'),
                description = item.get('description'),
                price = item.get('price'),
                user = self.context['request'].user
            )
            incomes.append(income)
            
        Income.objects.bulk_create(incomes)
        return incomes

    class Meta:
        model = Income
        fields = ['items']
class ListIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'name', 'description', 'price']
        extra_kwargs = {
            'name': {'required': False},
            'description': {'required': False},
            'price': {'required':False}
        }
class IncomeToWalletItem(serializers.Serializer):
    wallet = serializers.IntegerField(required = True)
    name = serializers.CharField(required = True, max_length = 255)
    description = serializers.CharField(max_length = 255)
    price = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators = [
            MinValueValidator(0.00)
        ],
        required = True
    )
    class Meta:
        fields = ['wallet', 'name','description','price']

class AddIncomeToWalletSerializer(serializers.Serializer):
    items = serializers.ListField(
        child = IncomeToWalletItem()
    )

    def save(self):
        incomeWallets = []
        items = self.validated_data.get('items')
        for item in items:
            try:
                wallet = Wallet.objects.get(pk = item.get('wallet'), user = self.context['request'].user)
            except:
                raise exceptions.NotFound(f'Not found wallet')
            income = Income(
                name = item.get('name'),
                description = item.get('description'),
                price = item.get('price'),
                user = self.context['request'].user
            )
            income.save()
            incomeWallet = IncomeWallet(
                income = income,
                wallet = wallet
            )
            incomeWallets.append(incomeWallet)
        IncomeWallet.objects.bulk_create(incomeWallets)
        return incomeWallets