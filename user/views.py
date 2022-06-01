from django.shortcuts import render
from user.serializers import CreateUserSerializer, EmailSerializer,RecoverPasswordSerializer
from django.db import transaction, utils
from rest_framework import generics, permissions, status, exceptions
from rest_framework.response import Response
from shared.utils import response_data, get_user_by_email, send_mail, age, generate_user_token
from user.models import UserToken
from jars.models import JarChoice, Jar
from django.utils import timezone
# Create your views here.
class CreateUserView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateUserSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
            Register user, send verify code to user email
        """
        serializer = CreateUserSerializer(data = request.data)
        # data = {}
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        # data['response'] = 'Registed successfully a new user.'
        # data['message'] = 'Please check your email to see your verification code'
        # data['email'] = user.email
        
        #set up mail
        user_token = UserToken.objects.filter(user = user).values('verifyCode').order_by('-id').first()
        subject = 'Welcome to Financial Management'
        body = '<p>Below is verification code of your account.</p><h4>' + user_token['verifyCode'] + '</h4>'
        to_email = user.email
        
        email_data = { 'subject': subject, 'body': body, 'to_email': to_email }

        try:
            send_mail(email_data)
        except exceptions.APIException as e:
            response = response_data(
                success = False,
                statusCode = status.HTTP_503_SERVICE_UNAVAILABLE,
                message = 'Error while sending email',
                data = e.detail
            )
            return Response(response, response.get('statusCode'))
                
        response = response_data(
            success = True,
            statusCode = status.HTTP_201_CREATED,
            message = 'Registered account successfully. Please check email to get verify code',
            data = serializer.data
        )
        return Response(response, status = response.get('statusCode'))


class Test(generics.ListCreateAPIView):
    def list(self, request, *args, **kwargs):
        user = request.user
        dob = user.dob
        print(dob)
        print(age(dob))

        return Response()


class VerifyEmailView(generics.UpdateAPIView):
    serializer_class = EmailSerializer
    permission_classes = [permissions.AllowAny]

    def create_jars(self, user, percentNEC, percentFFA, percentLTTS, percentPlay, percentGive, percentEdu):
        jars = []
        jarNEC = Jar(
            name = JarChoice.NEC,
            percent = percentNEC,
            user = user
        )
        jars.append(jarNEC)
        jarFFa = Jar(
            name = JarChoice.FFA,
            percent = percentFFA,
            user = user
        )
        jars.append(jarFFa)
        jarLTSS = Jar (
            name = JarChoice.LTSS,
            percent = percentLTTS,
            user = user
        )
        jars.append(jarLTSS)
        jarEDU  = Jar(
            name = JarChoice.EDU,
            percent = percentEdu,
            user = user
        )
        jars.append(jarEDU)
        jarPlay = Jar(
            name = JarChoice.PLAY,
            percent = percentPlay,
            user = user
        )
        jars.append(jarPlay)
        jarGive = Jar(
            name = JarChoice.GIVEN,
            percent = percentGive,
            user = user
        )
        jars.append(jarGive)
        Jar.objects.bulk_create(jars)
    
    def put(self, request, *args, **kwargs):
        print(request.data)
        """
            Check verify code and activate user email to login
        """
        # response = {}
        user = get_user_by_email(request.data['email'])
        
        if user is None:
            raise exceptions.NotFound()
        dob = user.dob
        print(age(dob))
        user_token = UserToken.objects.filter(user = user).order_by('-id').first()
        # if user_token is None:
        #     return Response(data = 'Not found user', status = status.HTTP_404_NOT_FOUND)

        current = timezone.now()
        
        if user_token.isVerified:
            return Response(
                response_data(
                    success = True,
                    statusCode = status.HTTP_202_ACCEPTED,
                    message = 'Your account has been verified before'
                )
            )
        response = response_data(
            success = True
        )
        if user_token.expiredAt > current and user_token.verifyCode == request.data.get('verifyCode', ''):
            user.is_active = True
            user_token.isVerified = True
            user.save(update_fields = ['is_active'])
            user_token.save(update_fields = ['isVerified'])
            response['statusCode'] = status.HTTP_202_ACCEPTED
            response['message'] = 'Verified successfully'
            if (age(user.dob) > 18 and age(user.dob) < 30):
                percentNEC = 50
                percentFFA = 5
                percentLTTS = 15
                percentEDU = 15
                percentPlay = 10
                percentGive = 5
                self.create_jars(user, percentNEC, percentFFA, percentLTTS, percentPlay, percentGive, percentEDU)
            if(age(user.dob) > 30 and age(user.dob) < 60):
                percentNEC = 50
                percentFFA = 10
                percentLTTS = 15
                percentEDU = 5
                percentPlay = 10
                percentGive = 10
                self.create_jars(user, percentNEC, percentFFA, percentLTTS, percentPlay, percentGive, percentEDU)
            if(age(user.dob) > 60):
                percentNEC = 40
                percentFFA = 20
                percentLTTS = 15
                percentEDU = 2
                percentPlay = 13
                percentGive = 10
                self.create_jars(user, percentNEC, percentFFA, percentLTTS, percentPlay, percentGive, percentEDU)
        else:
            response['statusCode'] = status.HTTP_400_BAD_REQUEST
            response['message'] = 'The code is not matched or expired'
        
        return Response(response, status = response.get('statusCode'))

class CheckEmailForgotPassword(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    
    def put(self, request, *args, **kwargs):
        user = get_user_by_email(request.data.get('email'))
        if user is None:
            raise exceptions.NotFound()
        user_token = UserToken.objects.filter(user = user, isVerified = False).order_by('-createdAt').first()
        current = timezone.now()
        # If token is not expired, return it else create new ones
        if user_token and user_token.expiredAt > current:
            token = user_token.verifyCode
        else:
            token = generate_user_token(user)
        email_data = {}
        email_data['subject']= "Reset Password"
        email_data['body'] = f"Your verify code is {token}"
        email_data['to_email'] = user.email
        send_mail(email_data)
        response = response_data(
            success = True,
            statusCode = status.HTTP_200_OK,
            message = "Your email is existed",
            data = {
                'email': user.email,
                'expiredAt': token.expiredAt if not user_token else user_token.expiredAt
            }
        )
        return Response(response, status = response.get('statusCode'))

class RecoverPassword(generics.UpdateAPIView):
    serializer_class = RecoverPasswordSerializer
    permission_classes = [permissions.AllowAny]
    def update(self, request, *args, **kwargs):
        user_from_db = get_user_by_email(request.data.get('email'))
        if user_from_db is None:
            raise exceptions.NotFound()
        serializer = self.get_serializer(data=request.data, context = { 'request': request })
        serializer.is_valid(raise_exception = True)
        serializer.update(user_from_db, serializer.validated_data)
        response = response_data(
            success = True,
            statusCode = status.HTTP_200_OK,
            message = f'Recover password of email {user_from_db.email} successfully'
        )
        return Response(response, status = response.get('statusCode'))

class VerifyCodeForRetrivePasswordView(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    def put(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = get_user_by_email(request.data['email'])
        if user is None:
            raise exceptions.NotFound()
        user_token = UserToken.objects.filter(user = user).order_by('-id').first()
        # if user_token is None:
        #     return Response(data = 'Not found user', status = status.HTTP_404_NOT_FOUND)

        current = timezone.now()
        
        if user_token.isVerified:
            return Response(
                response_data(
                    success = True,
                    statusCode = status.HTTP_202_ACCEPTED,
                    message = 'Your account has been verified before'
                )
            )
        response = response_data(
            success = True
        )
        if user_token.expiredAt > current and user_token.verifyCode == request.data.get('verifyCode', ''):
            user.is_active = True
            user_token.isVerified = True
            user.save(update_fields = ['is_active'])
            user_token.save(update_fields = ['isVerified'])
            response['statusCode'] = status.HTTP_202_ACCEPTED
            response['message'] = 'Verified successfully'
        else:
            response['statusCode'] = status.HTTP_400_BAD_REQUEST
            response['message'] = 'The code is not matched or expired'
        
        return Response(response, status = response.get('statusCode'))