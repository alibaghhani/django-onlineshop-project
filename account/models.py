from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from core.models import TimeStampMixin,LogicalDeleteMixin
# Create your models here.
class User(AbstractUser):
    """
    custom User model

    -----fields-----
    first_name = models.CharField()
    last_name = models.CharField()
    email = models.EmailField()
    """


    email_validator = RegexValidator(
        regex = r"^[a-zA-Z0-9._%+-]+@gmail\.com$",
        message = 'لطفا یک ایمیل درست وارد کنید'
    )
    # phone_number_validator = RegexValidator(
    #     regex = r"^09[0|1|2|3][0-9]{8}$"
    # )

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250,validators=[email_validator],unique=True)
    username = None

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    #phone_number = models.CharField(max_length=250,validators=[phone_number_validator])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return self.first_name