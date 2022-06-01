from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from shared.utils import response_data
from auth_jwt.serializers import MyTokenObtainPairSerializer
from rest_framework import permissions
# Create your views here.

class CustomTokenObtainView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MyTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context = { 'request': request })

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            # print(list(e))
            raise InvalidToken(e.args[0])
        # except AttributeError as e:
        #     print(e.args[0])
        #     raise AuthenticationFailed()
        response = response_data(
            success = True,
            statusCode = status.HTTP_201_CREATED,
            message = 'Log in successfully',
            data = serializer.validated_data
        )
        
        return Response(response, status = response.get('statusCode'))