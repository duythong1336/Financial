from django.shortcuts import render
from rest_framework import generics, status, exceptions
from jars_outcome.models import JarOutcome
from shared.utils import response_data
from jars.models import Jar
from jars.serializers import JarsSerializer, AddOutcomesToJar,OutComeInJar
from shared.messages import ResponseMessage
from rest_framework.response import Response
from out_come.models import OutCome
# Create your views here.
class GetJarsFollowUserView(generics.ListAPIView):

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = Jar.objects.filter(user = user)
        if len(queryset) > 0:
            serializer = JarsSerializer(queryset, many = True)
            response = response_data(
                success= True,
                statusCode= status.HTTP_200_OK,
                message= ResponseMessage.GET_SUCCESS_MESSAGE,
                data = serializer.data
            )
        else:
            response = response_data(
                success=False,
                statusCode=status.HTTP_400_BAD_REQUEST,
                message=ResponseMessage.GET_FAILURE_MESSAGE,
                
            )
        return Response(response,status = response.get('statusCode') )

class GetUpdateJarsView(generics.RetrieveUpdateAPIView):

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.pop('pk')
        try:
            queryset = Jar.objects.get(pk = pk, user = request.user)
        except:
            raise exceptions.NotFound({ 'errors': [f'Not found salon Branch with id {pk}'] })
        serializer = JarsSerializer(queryset)
        outcomes = OutCome.objects.filter(jars__jar = queryset)
        price = 0
        for item in list(outcomes):
            price += item.price
        
        data = serializer.data
        data['price'] = price
        response = response_data(
            success=True,
            statusCode=status.HTTP_200_OK,
            message = ResponseMessage.GET_SUCCESS_MESSAGE,
            data = data
        )
        return Response(response, status = response.get('statusCode'))

class AddOutcomeToJar(generics.ListCreateAPIView):
    def create(self, request, *args, **kwargs):
        jar_id = kwargs.pop('pk')
        try:
            jar = Jar.objects.get(pk = jar_id)
        except:
            raise exceptions.NotFound({'errors': [f'Not found Jar with id {jar_id}']})
        data = request.data
        print(data)
        serializer = AddOutcomesToJar(data = request.data, context = {'request': request, 'jar': jar})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = response_data(
                success=True,
                statusCode=status.HTTP_201_CREATED,
                message = ResponseMessage.CREATE_SUCCESS_MESSAGE,
                data = serializer.data
            )
        else:
            response = response_data(
                success = False,
                statusCode = status.HTTP_400_BAD_REQUEST,
                message = ResponseMessage.CREATE_FAILURE_MESSAGE,
                data = serializer.errors
            )
        return Response(response, status = response.get('statusCode'))
    
    def list(self, request, *args, **kwargs):
        jar_id = kwargs.pop('pk')
        try:
            jar = Jar.objects.get(pk = jar_id)
        except:
            raise exceptions.NotFound({'errors': [f'Not found Jar with id {jar_id}']})
        jaroutcome = JarOutcome.objects.filter(jar = jar, isDeleted = False)
        serializer = OutComeInJar(jaroutcome, many = True)
        response = response_data(
            success=True,
            statusCode=status.HTTP_200_OK,
            message = ResponseMessage.GET_SUCCESS_MESSAGE,
            data = serializer.data
        )
        return Response(response, status =  response.get('statusCode'))


        
