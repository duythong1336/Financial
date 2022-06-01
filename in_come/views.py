from asyncio import exceptions
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from in_come.models import Income
from shared.utils import response_data
from shared.messages import ResponseMessage
from in_come.serializers import CreateIncomeSerializer,ListIncomeSerializer
# Create your views here.
class CreateAndListIncomeView(generics.ListCreateAPIView):
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = CreateIncomeSerializer(data = data, context = {'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = response_data(
            success = True,
            statusCode=status.HTTP_201_CREATED,
            message=ResponseMessage.CREATE_SUCCESS_MESSAGE,
            data = serializer.data
        )
        else:
            response = response_data(
                success = False,
                statusCode=status.HTTP_400_BAD_REQUEST,
                message=ResponseMessage.CREATE_FAILURE_MESSAGE
            )
        return Response(response, status=response.get('statusCode'))

    def list(self, request, *args, **kwargs):
        queryset = Income.objects.filter(user = request.user)
        if len(queryset) > 0:
            serializer = ListIncomeSerializer(queryset, many = True)
            response = response_data(
                success = True,
                statusCode=status.HTTP_200_OK,
                message= ResponseMessage.GET_SUCCESS_MESSAGE,
                data = serializer.data
            )
        else:
            response = response_data(
                success = False,
                statusCode=status.HTTP_400_BAD_REQUEST,
                message=ResponseMessage.GET_FAILURE_MESSAGE
            )
        return Response(response, status= response.get('statusCode'))
    
class GetDetailUpdateIncomeView(generics.RetrieveUpdateAPIView):
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.pop('pk')
        queryset = Income.objects.get(pk = pk)
        if queryset is not None:
            serializer = ListIncomeSerializer(queryset)
            response = response_data(
                success = True,
                statusCode=status.HTTP_200_OK,
                message= ResponseMessage.GET_SUCCESS_MESSAGE,
                data = serializer.data
            )
        else:
            response = response_data(
                success = False,
                statusCode=status.HTTP_400_BAD_REQUEST,
                message=ResponseMessage.GET_FAILURE_MESSAGE
            )
        return Response(response, status= response.get('statusCode'))
    
    def update(self, request, *args, **kwargs):
        id = kwargs.pop('pk')
        partial = kwargs.pop('partial', False)
        income = Income.objects.get(
            pk = id,
             
        )
        serializer = ListIncomeSerializer(income, data=request.data, partial = partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if getattr(income, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            income._prefetched_objects_cache = {}
        response = response_data(
            success = True,
            statusCode = status.HTTP_200_OK,
            message = ResponseMessage.UPDATE_SUCCESS_MESSAGE,
            data = serializer.data
        )
        return Response(response, status = response.get('statusCode'))


class GetlistIncomeEnableAddtoWallet(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        queryset = Income.objects.filter(user = request.user).exclude(wallets__income__user = request.user)
        if len(queryset) > 0:
            serializer = ListIncomeSerializer(queryset, many=True)
            response = response_data(
                success = True,
                statusCode=status.HTTP_200_OK,
                message= ResponseMessage.GET_SUCCESS_MESSAGE,
                data = serializer.data
            )
        else:
            response = response_data(
                success = False,
                statusCode=status.HTTP_200_OK,
                message=ResponseMessage.GET_SUCCESS_MESSAGE,
                data = []
            )
        return Response(response, status= response.get('statusCode'))

