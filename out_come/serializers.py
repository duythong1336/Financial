from asyncio.format_helpers import extract_stack
from asyncore import read
from logging.config import valid_ident
from rest_framework import serializers
from out_come.models import OutCome
from django.core.validators import MinValueValidator
from django.utils.timezone import now
from jars_outcome.models import JarOutcome
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
    id = serializers.IntegerField(required = False, read_only = True)
    class Meta:
        fields = ['name', 'description', 'price','date', 'id']
        
class CreateOutComeSerializer(serializers.ModelSerializer):
    def save(self):
        
        outcome = OutCome(
            name = self.validated_data['name'],
            description = self.validated_data['description'],
            price = self.validated_data['price'],
            user = self.context['request'].user,
            date = self.validated_data['date'],
        )
        
            
        outcome.save()
        return outcome

    class Meta:
        model = OutCome
        fields = ['id', 'name', 'description', 'price', 'date']
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
    
class OutComeWithJarSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        temp_dict = {}
        try:
            jar = instance.jars.all().first()
            temp_dict['jarId'] = jar.jar.id
            temp_dict['jarName'] = jar.jar.name
            temp_dict['id'] = instance.id
            temp_dict['name'] = instance.name
            temp_dict['description'] = instance.description
            temp_dict['price'] = instance.price
            temp_dict['date'] = instance.date     
        except:
            temp_dict['id'] = instance.id
            temp_dict['name'] = instance.name
            temp_dict['description'] = instance.description
            temp_dict['price'] = instance.price
            temp_dict['date'] = instance.date
        return temp_dict

class UpdateJarForOutComeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JarOutcome
        fields = ['jar', 'outcome']
    
    def update(self):
        jar = self.validated_data.get('jar')
        outcome = self.validated_data.get('outcome')
        try:
            jaroutcome = JarOutcome.objects.get(outcome = outcome)
            jaroutcome.jar = jar
            print(jaroutcome)
            jaroutcome.save(update_fields = ['jar'])
        except:
            item = JarOutcome(
                jar = jar,
                outcome = outcome,
                price = outcome.price
            )
            item.save()
