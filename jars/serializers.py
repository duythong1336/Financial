from rest_framework import serializers, exceptions
from jars.models import JarChoice, Jar
from out_come.models import OutCome
from jars_outcome.models import JarOutcome
class JarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jar
        fields = ['id', 'name', 'percent']

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

