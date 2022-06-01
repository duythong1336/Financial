from urllib import response
from django.shortcuts import render
from rest_framework import generics, status, exceptions
from shared.utils import response_data
from shared.messages import ResponseMessage
from wallet.serializers import CreateWalletSerializer,WalletSerialzier,IncomeInWalletSerializer,AddIncomeToWalletSerializer
from rest_framework.response import Response
from wallet.models import Wallet
from income_wallet.models import IncomeWallet
from in_come.models import Income
# Create your views here.


class CreateGetWalletFollowUserView(generics.ListCreateAPIView):
   
    def create(self, request, *args, **kwargs):
        print(request.user)
        serializer = CreateWalletSerializer(data = request.data, context = {'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()

            response = response_data(
                success = True,
                statusCode=status.HTTP_201_CREATED,
                message = ResponseMessage.CREATE_SUCCESS_MESSAGE,
                data = serializer.data
            )
        except exceptions.APIException as exc:
            raise exceptions.ValidationError(exc.detail)
            
        return Response(response, status = response.get('statusCode'))
    
    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = Wallet.objects.filter(
            user = user
        )
        if len(queryset) > 0:
            serializer = WalletSerialzier(queryset, many = True)
            response = response_data(
                success= True,
                statusCode=status.HTTP_200_OK,
                message=ResponseMessage.GET_SUCCESS_MESSAGE,
                data = serializer.data
            )
        else:
            response = response_data(
                success= True,
                statusCode=status.HTTP_200_OK,
                message= 'Not found any wallet this user'
            )
        return Response(response, status = response.get('statusCode'))
class GetDetailUpdateWalletView(generics.RetrieveUpdateAPIView):
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.pop('pk')
        try:
            wallet = Wallet.objects.get(pk = pk)
        except:
            raise exceptions.NotFound(f'Not found wallet with id {pk}')
        incomes = Income.objects.filter(wallets__wallet = wallet)
        serializer = WalletSerialzier(wallet)
        data = serializer.data
        if len(incomes) > 0:
            price = 0
            for item in list(incomes):
                price += item.price
            data['price'] = price
        
        response = response_data(
            success=True,
            statusCode=status.HTTP_200_OK,
            message=ResponseMessage.GET_SUCCESS_MESSAGE,
            data = data
        )
        return Response(response, status = response.get('statusCode'))
    
    def update(self, request, *args, **kwargs):
        pk = kwargs.pop('pk')
        partial = kwargs.pop('partial', False)
        try:
            wallet = Wallet.objects.get(pk = pk)
        except:
            raise exceptions.NotFound(f'Not found wallet with id {pk}')
        serializer = WalletSerialzier(wallet, data=request.data, partial = partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if getattr(wallet, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            wallet._prefetched_objects_cache = {}
        response = response_data(
            success = True,
            statusCode = status.HTTP_200_OK,
            message = ResponseMessage.UPDATE_SUCCESS_MESSAGE,
            data = serializer.data
        )
        return Response(response, status = response.get('statusCode'))


class AddIncomeToWallet(generics.ListCreateAPIView):
    def create(self, request, *args, **kwargs):
        wallet_id = kwargs.pop('pk')
        try:
            wallet = Wallet.objects.get(pk = wallet_id)
        except:
            raise exceptions.NotFound({'errors': [f'Not found wallet with id {wallet_id}']})
        serializer = AddIncomeToWalletSerializer(data = request.data, context = {'request': request, 'wallet': wallet})
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
        wallet_id = kwargs.pop('pk')
        try:
            wallet = Wallet.objects.get(pk = wallet_id)
        except:
            raise exceptions.NotFound({'errors': [f'Not found Wallet with id {wallet_id}']})
        walletincome = IncomeWallet.objects.filter(wallet = wallet, isDeleted = False)
        serializer = IncomeInWalletSerializer(walletincome, many = True)
        response = response_data(
            success=True,
            statusCode=status.HTTP_200_OK,
            message = ResponseMessage.GET_SUCCESS_MESSAGE,
            data = serializer.data
        )
        return Response(response, status =  response.get('statusCode'))