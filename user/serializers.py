from rest_framework import serializers, exceptions
from user.models import User, UserToken
from django.db import transaction
import uuid
import os
from shared.utils import generate_user_token, get_user_by_email, generate_verify_code
from django.utils import timezone
class CreateUserSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(write_only = True)
    
    
    class Meta:
        model = User
        fields = [
            'email', 'password', 'password2', 
            'firstName', 'lastName', 'phoneNumber', 'dob', 
            'gender', 'address']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    # User registration process
    @transaction.atomic
    def save(self):
        """
            Save user to db. Check if password is matched.
            default group: CUSTOMER
            default expiry interval: 15 minutes
        """
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({
                'password': 'Passwords must be matched'
            })
            
        user = User(
            email = self.validated_data['email'],
            phoneNumber = self.validated_data['phoneNumber'],
            firstName = self.validated_data['firstName'],
            lastName = self.validated_data['lastName'],
            address = self.validated_data['address'],
            dob = self.validated_data['dob'],
            code = str(uuid.uuid4()),
            is_active = False,
        )

        user.set_password(password)
        # code = generate_verify_code()
        # expiry_interval = timezone.tiUserTokenmedelta(minutes = int(os.environ.get('EXPIRY_INTERVAL', 15)))
        # expiry_time = timezone.now() + expiry_interval
        
        # user_token = UserToken(
        #     # verify_code = code,
        #     verify_code = code, # bypass for dev
        #     expired_at = expiry_time,
        # )
        
        user.save()
        generate_user_token(user)
        # user.tokens.add(user_token)
        
        return user
class ProfileSerializer(serializers.ModelSerializer):
    
    gender = serializers.CharField(
        required = False
    )
    dob = serializers.DateField(required = False)  
    
    def update(self, instance, validated_data):
        """
            Update first name, last name, dob, address, phone_number, gender
        """
        

        update_fields = []
        for key, value in validated_data.items():
            # print('Key: ', key)
            # print('Value: ', value)
            if hasattr(instance, key):
                setattr(instance, key, value)  
                update_fields.append(key)
        
        instance.save(update_fields = update_fields)
        return instance
    
    class Meta:
        model = User
        fields = [ 'firstName', 'lastName', 'address', 'phoneNumber', 'dob', 'gender', 'email', 'id']
        extra_kwargs = {
            'email': {
                'read_only': True
            },
            'id': {
                'read_only': True
            },
            'firstName': {
                'required': False
            },
            'lastName': {
                'required': False
            },
            'address': {
                'required': False
            }
        }

class EmailSerializer(serializers.ModelSerializer):
    
    newEmail = serializers.EmailField(write_only = True)
    

    def validate(self, attrs):
        errors = {}
        for key, value in attrs.items():
            print(f'Key: {key} -- Value: {value}')
        
        user_from_db = get_user_by_email(attrs.get('newEmail'))
        
        if user_from_db is not None and user_from_db.is_active: # new email is existed
            errors['newEmail'] = f'{user_from_db.email} already exists.'
            err = exceptions.ValidationError(errors)
            raise err
        
        return super().validate(attrs)
    
    class Meta:
        model = User
        fields = [ 'newEmail' ]