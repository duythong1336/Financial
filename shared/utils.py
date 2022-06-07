
from user.models import User, UserToken
from rest_framework import exceptions
from django.utils import timezone
import smtplib, os
from django.core.mail import EmailMessage


def get_user_by_email(email):
        try:
            return User.objects.get(email = email)
        except User.DoesNotExist:
            # raise exceptions.NotFound(detail = f'Not found user with email {email}')
            return None
        
def generate_user_token(user, timedelta = 15):
    """
        Platform MOBILE by default
        
        Expired time delta 15 minutes by default
    """
    user_token = UserToken(
            # verifyCode = generate_verify_code(),
            verifyCode = '123456', # bypass for dev
            expiredAt = timezone.now() + timezone.timedelta(minutes = int(os.environ.get('EXPIRY_INTERVAL', timedelta))),
            user = user,
        )
    user_token.save()
    return user_token

def generate_verify_code():
    
    import math, random
    
    digits = '0123456789'
    code = ''
    for i in range(6):
        code += digits[math.floor(random.random() * 10)]
        
    return code

def response_data(success: bool = False, statusCode = None, message: str = None, data = None):
    return {
        'success': success,
        'statusCode': statusCode,
        'message': message,
        'data': data if isinstance(data, dict) or isinstance(data, list) else []
    }
def check_valid_token(user, verify_code_from_input):
    
    
    user_token = user.tokens.all().order_by('-createdAt').first()
    
    now = timezone.now()
    
    if user_token.verifyCode != verify_code_from_input or len(verify_code_from_input) != 6:
        error = exceptions.ValidationError({}, 'token_invalid')
        error.default_detail = 'Verification code is invalid'
        raise error
    
    if user_token.expiredAt < now:
        error = exceptions.ValidationError({}, 'token_expired')
        error.default_detail = 'Verification code is expired'
        raise error
    
    if user_token.isVerified:
        error = exceptions.ValidationError({}, 'token_is_verified')
        error.default_detail = 'Verification code has been used before'
        raise error
    
    # if user_token is valid
    user_token.isVerified = True
    user_token.save(update_fields = ['isVerified'])
    return True

def generate_verify_code():
    
    import math, random
    
    digits = '0123456789'
    code = ''
    for i in range(6):
        code += digits[math.floor(random.random() * 10)]
        
    return code

def send_mail(data):
    message = EmailMessage(
        subject = data['subject'],
        body = data['body'],
        to = [data['to_email']],
    )
    message.content_subtype = 'html'
    
    try:
        message.send(fail_silently = True)
    except smtplib.SMTPException as exc:
        print(str(exc))
        return exc

from datetime import date
 
def age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def format_str_to_date_v2(str_date):
    """
    Validate date format of string
    
    Return: string with date format
    """
    from datetime import datetime
    format = f"%Y-%m-%d"
    try:
        date = datetime.strptime(str_date, format)
        return date
    except Exception as ex:
        print(ex)
        raise exceptions.ValidationError({'date': ['Invalid format. Format: yyyy-MM-dd']})