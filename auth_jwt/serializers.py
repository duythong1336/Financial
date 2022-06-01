from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group, update_last_login
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.settings import api_settings
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions, status, serializers
from shared.utils import response_data, get_user_by_email
from shared.exception import models as custom_exceptions
from user.serializers import ProfileSerializer

class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('style', {})

        kwargs['style']['input_type'] = 'password'
        kwargs['write_only'] = True

        super().__init__(*args, **kwargs)

class TokenObtainSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD

    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials'),
        'forbidden': _('Forbidden. Permissions denied')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.EmailField()
        self.fields['password'] = PasswordField()
        # self.fields['location'] = serializers.CharField(required = False)
    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password']
            # 'location': attrs['location'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        # self.user = authenticate(**authenticate_kwargs)
        
        request = self.context.get('request')
        
        self.user = get_user_by_email(request.data.get('email'))
        
        if self.user is None:
            raise custom_exceptions.InvalidUserError('Wrong email or password')
        
        valid_password = self.user.check_password(request.data.get('password')) # boolean
        if not valid_password:
            raise custom_exceptions.InvalidUserError('Wrong email or password')
        
        if not self.user.is_active:
            raise custom_exceptions.InvalidUserError('Please verify your mail')
            
        
        
        
        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        return {}

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)


class MyTokenObtainPairSerializer(TokenObtainSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        # data.pop('refresh', None)
        data['accessToken'] = str(refresh.access_token)
        data['info'] = ProfileSerializer(self.user).data
        
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['is_active'] = user.is_active
        token['email'] = user.email
        token['firstName'] = user.first_name
        token['lastName'] = user.last_name
        # ...
        group_qs = Group.objects.filter(user=user).values('name')
        groups = [ group.get('name') for group in group_qs ]
        token['groups'] = groups
        return token