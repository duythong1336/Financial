from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from shared.models import BaseModel, SoftDeleteModel
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
# Create your models here.
class Gender(models.TextChoices):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

class User(AbstractUser, BaseModel, SoftDeleteModel):
    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    email = models.EmailField(
        max_length=  255,
        unique = True
    )
    REQUIRED_FIELDS = []
    firstName = models.CharField(
        max_length = 15,
        validators= [
            MinLengthValidator(2),
            MaxLengthValidator(15)
        ]
    )

    lastName = models.CharField(
        max_length= 15,
        validators= [
            MinLengthValidator(2),
            MaxLengthValidator(15)
        ],
    )
    phoneNumber = models.CharField(
        max_length = 20,
        validators= [
            RegexValidator(
                regex = '(03|05|07|08|09|01[2|6|8|9])+([0-9]{8})',
                message= 'invalid format number. Example: 0859325039 '
            )
        ],
        default= ''
    )
    address = models.CharField(
        max_length= 255
    )
    dob = models.DateField(null=True)
    gender = models.CharField(
        max_length=10,
        choices= Gender.choices,
        default= Gender.OTHER
    )
    code = models.CharField(max_length= 255, unique=True)

    def __str__(self):
        return self.email
class UserToken(SoftDeleteModel, BaseModel):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'tokens')
    verifyCode = models.CharField(
        max_length = 6,
        validators = [
            MinLengthValidator(6),
            MaxLengthValidator(6),
        ]
    )
    
    expiredAt = models.DateTimeField(
        editable = False,
    )
    
    isVerified = models.BooleanField(default = False)
    
    def __str__(self):
        return self.verifyCode