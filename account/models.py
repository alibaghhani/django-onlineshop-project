from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from core.models import TimeStampMixin,LogicalDeleteMixin
from .manager import UserManager

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

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    #phone_number = models.CharField(max_length=250,validators=[phone_number_validator])

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Address(models.Model):
        """
        address model for adding user's addresses
        """

        costumer = models.ForeignKey('User',on_delete=models.CASCADE,related_name='costumer_address')
        province = models.CharField(max_length=25)
        city = models.CharField(max_length=30)
        street = models.CharField(max_length=250)
        alley = models.CharField(max_length=250)
        house_number = models.CharField(max_length=4)
        full_address = models.CharField(max_length=250)

        def __str__(self):
            return f"{self.province} {self.city}"




