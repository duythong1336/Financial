from asyncio.format_helpers import extract_stack
from rest_framework import serializers
from out_come.models import OutCome
from django.core.validators import MinValueValidator
from django.utils.timezone import now
class OutComeItemSerializer(serializers.Serializer):
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
    date = serializers.DateField(required = False, default = now )
    class Meta:
        fields = ['name', 'description', 'price','date']
        
class CreateOutComeSerializer(serializers.Serializer):
    items = serializers.ListField(
        child = OutComeItemSerializer()
    )
    def save(self):
        outcomes = []
        items = self.validated_data['items']
        for item in items:
            outcome = OutCome(
                name = item.get('name'),
                description = item.get('description'),
                price = item.get('price'),
                user = self.context['request'].user,
                date = item.get('date')
            )
            outcomes.append(outcome)
            
        OutCome.objects.bulk_create(outcomes)
        return outcomes

    class Meta:
        model = OutCome
        fields = ['items']
class ListOutComeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutCome
        fields = ['id', 'name', 'description', 'price','date']
        extra_kwargs = {
            'name': {'required': False},
            'description': {'required': False},
            'price': {'required': False},
            'date': {'required': False},
        }
    
