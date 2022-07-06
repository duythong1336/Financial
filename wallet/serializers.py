from doctest import debug_script
from rest_framework import serializers, exceptions
from wallet.models import Wallet
from in_come.models import Income
from income_wallet.models import IncomeWallet
class CreateWalletSerializer(serializers.ModelSerializer):
    
    
    def save(self):
        print(self.context['request'].user)
        wallet = Wallet(
            user = self.context['request'].user,
            name = self.validated_data['name'],
            price = self.validated_data['price'],
            description = self.validated_data['description']
        )
        wallet.save()
        return wallet
    class Meta:
        model = Wallet
        fields = ['name', 'price', 'description']

class ItemWalletSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    class Meta:
        fields = ['name', 'description']

class CreateWalletSerializer(serializers.Serializer):
    
    items = serializers.ListSerializer(
        child = ItemWalletSerializer()
    )

    def save(self):
        user = self.context['request'].user
        input_wallets = self.validated_data.get('items')
        new_list = []
        for item in input_wallets:
            temp = Wallet(
                user = user,
                name = item.get('name'),
                description = item.get('description'),
            )
            new_list.append(temp)
        Wallet.objects.bulk_create(new_list)
    class Meta:
        fields = ['items']
class WalletSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'name', 'description', 'price']
        extra_kwargs = {
            'name': {'required': False},
            'description': {'required': False},
            'price': {'required': False}
        }
class WalletWithPriceSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        price = 0
        temp_dict = {}
        incomes = instance.incomes.filter(wallet = instance)
        if len(incomes) > 0:
            for item in list(incomes):
                price += item.income.price
        else:
            price = 0
        temp_dict['id'] = instance.id
        temp_dict['name'] = instance.name
        temp_dict['description'] = instance.description
        temp_dict['price'] = price
        return temp_dict
class AddIncomeToWalletSerializer(serializers.Serializer):
    incomes = serializers.ListSerializer(
        child = serializers.IntegerField()
    )
    class Meta:
        fields = ('incomes')
    
    def save(self):
        incomesRequest = self.validated_data.get('incomes',None)
        walletincomes = []
        wallet = self.context['wallet']
        for income in incomesRequest:
            try:
                income = Income.objects.get(pk = income, user = self.context['request'].user)
            except:
                raise exceptions.NotFound({'errors': [f'Not found Jar with id {income}']})
            incomewallet = IncomeWallet(
                wallet = wallet,
                income = income
            )
            walletincomes.append(incomewallet)
        
        IncomeWallet.objects.bulk_create(walletincomes)
        return walletincomes

class IncomeInWalletSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        
        income = instance.income

        return{
            "walletName": instance.wallet.name,
            "walletId": instance.wallet.id,
            "incomeId": income.id,
            "incomeName": income.name,
            'incomePrice': income.price,
            'incomeDate': income.date,
            "incomeDescription": income.description
        }