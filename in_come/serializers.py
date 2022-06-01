from abc import update_abstractmethods
from rest_framework import serializers
from in_come.models import Income
from django.core.validators import MinValueValidator

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
