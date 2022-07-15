from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from out_come.models import OutCome
from shared.utils import response_data, format_str_to_date_v2
from shared.messages import ResponseMessage
from out_come.serializers import CreateOutComeSerializer,ListOutComeSerializer,OutComeWithJarSerializer,UpdateJarForOutComeSerializer
# Create your views here.
class CreateAndListOutComeView(generics.ListCreateAPIView):
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = CreateOutComeSerializer(data = data, context = {'request': request})
        if serializer.is_valid(raise_exception=True):
            outcome = serializer.save()
            data = serializer.data
            data['id'] = outcome.id
            response = response_data(
            success = True,
            statusCode=status.HTTP_201_CREATED,
            message=ResponseMessage.CREATE_SUCCESS_MESSAGE,
            data = data
        )
        else:
            response = response_data(
                success = False,
                statusCode=status.HTTP_400_BAD_REQUEST,
                message=ResponseMessage.CREATE_FAILURE_MESSAGE
            )
        return Response(response, status=response.get('statusCode'))

    def list(self, request, *args, **kwargs):
        from django.db.models import Q
        from datetime import datetime
        query = Q()

        fromDateStr = request.query_params.get('fromDate')
        if fromDateStr is not None:
            fromDate = format_str_to_date_v2(fromDateStr)
            query.add(Q(date__gte = fromDate), Q.AND)
        
        toDateStr = request.query_params.get('toDate', str(datetime.today().date()))
        if toDateStr is not None:
            toDate = format_str_to_date_v2(toDateStr)
            query.add(Q(date__lte = toDate), Q.AND)
        query.add(Q(user = request.user), Q.AND)
        queryset = OutCome.objects.filter(query)
        if len(queryset) > 0:
            serializer = OutComeWithJarSerializer(queryset, many = True)
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
class GetDetailUpdateOutComeView(generics.RetrieveUpdateAPIView):
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.pop('pk')
        queryset = OutCome.objects.get(pk = pk)
        if queryset is not None:
            serializer = ListOutComeSerializer(queryset)
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
        outcome = OutCome.objects.get(
            pk = id,
        )
        serializer = ListOutComeSerializer(outcome, data=request.data, partial = partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if getattr(outcome, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            outcome._prefetched_objects_cache = {}
        response = response_data(
            success = True,
            statusCode = status.HTTP_200_OK,
            message = ResponseMessage.UPDATE_SUCCESS_MESSAGE,
            data = serializer.data
        )
        return Response(response, status = response.get('statusCode'))

class GetlistOutcomeEnableAddtoJar(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        queryset = OutCome.objects.filter(user = request.user).exclude(jars__outcome__user = request.user)
        if len(queryset) > 0:
            serializer = ListOutComeSerializer(queryset, many = True)
            response = response_data(
                success = True,
                statusCode = status.HTTP_200_OK,
                message = ResponseMessage.GET_SUCCESS_MESSAGE,
                data = serializer.data
            )
        else:
            response = response_data(
                success = False,
                statusCode = status.HTTP_400_BAD_REQUEST,
                message = ResponseMessage.GET_FAILURE_MESSAGE,
                data = []
            )
        return Response(response, status = response.get('statusCode'))

class UpdateJarForOutComeView(generics.UpdateAPIView):
    def put(self, request, *args, **kwargs):
        serializer = UpdateJarForOutComeSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.update()
            response = response_data(
                success = True,
                statusCode = status.HTTP_200_OK,
                message = ResponseMessage.UPDATE_SUCCESS_MESSAGE,
                data = serializer.data
            )
        else:
            response = response_data(
                success = False,
                statusCode = status.HTTP_400_BAD_REQUEST,
                message = ResponseMessage.UPDATE_FAILURE_MESSAGE
            )
        return Response(response, status = response.get('statusCode'))