from rest_framework import serializers, exceptions
from jars.models import JarChoice, Jar
from out_come.models import OutCome
from jars_outcome.models import JarOutcome
class JarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jar
        fields = ['id', 'name', 'percent']

class JarAndPriceSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        price = 0
        temp_dict = {}
        outcomes = instance.outcomes.filter(jar = instance)
        if len(outcomes) > 0:
            for outcome in list(outcomes):
                price += outcome.outcome.price
        else:
            price = 0
        temp_dict['id'] = instance.id
        temp_dict['name'] = instance.name
        temp_dict['percent'] = instance.percent
        temp_dict['price'] = price
        
        return temp_dict
        
class RetrieveJarSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        outcomes = instance.outcomes.all()
        data = []
        for item in list(outcomes):
            temp_dict = {}
            temp_dict['id'] = item.outcome.id
            temp_dict['name'] = item.outcome.name
            temp_dict['price'] = item.outcome.price
            temp_dict['description'] = item.outcome.description
            temp_dict['date'] = item.outcome.date
            data.append(temp_dict)
        return{
            'jarId': instance.id,
            'jarName': instance.name,
            'outcomes': data
        }
class AddOutcomesToJar(serializers.Serializer):
    outcomes = serializers.ListSerializer(
        child = serializers.IntegerField()
    )
    class Meta:
        fields = ('outcomes')
    
    def save(self):
        outcomesRequest = self.validated_data.get('outcomes',None)
        jaroutcomes = []
        jar = self.context['jar']
        for outcome in outcomesRequest:
            try:
                outcome = OutCome.objects.get(pk = outcome, user = self.context['request'].user)
            except:
                raise exceptions.NotFound({'errors': [f'Not found Jar with id {outcome}']})
            jaroutcome = JarOutcome(
                jar = jar,
                outcome = outcome
            )
            jaroutcomes.append(jaroutcome)
        
        JarOutcome.objects.bulk_create(jaroutcomes)
        return jaroutcomes

class OutComeInJar(serializers.BaseSerializer):
    def to_representation(self, instance):
        
        outcome = instance.outcome
        return{
            "jarName": instance.jar.name,
            "jarId": instance.jar.id,
            "outcomeId": outcome.id,
            "outcomeName": outcome.name,
            "outcomeDescription": outcome.description
        }

class ItemUpdateJarSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    percent = serializers.IntegerField()
    class Meta:
        fields = ['id', 'percent']

class UpdateJarSerializer(serializers.Serializer):
    items = serializers.ListSerializer(
        child = ItemUpdateJarSerializer()
    )
    class Meta:
        fields = ['items']
    def save(self):
        jars = self.validated_data.get('items', None)
        for item in jars:
            jar = Jar.objects.get(id = item.get('id'))
            jar.percent = item.get('percent')
            jar.save(update_fields=['percent'])

