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
        regex = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
    )
    # phone_number_validator = RegexValidator(
    #     regex = r"^09[0|1|2|3][0-9]{8}$"
    # )

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250,validators=[email_validator])
    username = None

    #phone_number = models.CharField(max_length=250,validators=[phone_number_validator])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return self.first_name