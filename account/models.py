from django.contrib.auth.models import AbstractUser
from core.models import TimeStampMixin, LogicalDeleteMixin
from django.core.validators import RegexValidator
from django.db import models
from .manager import UserManager


# Create your models here.
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
        regex=r"^[a-zA-Z0-9._%+-]+@gmail\.com$",
        message='لطفا یک ایمیل درست وارد کنید'
    )
    username_validator = RegexValidator(
        regex=r'^(?=.*[A-Z]).{8,}$',
        message='Username must be at least 8 characters long and contain at least one uppercase letter.',
    )
    username = models.CharField(max_length=250, validators=[username_validator], unique=True, null=True, blank=True)
    email = models.EmailField(max_length=250, validators=[email_validator], unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    admin_name = models.CharField(max_length=250,null=True,blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['admin_name']

    def __str__(self):
        return f"{self.email}"

    def save(self, *args, **kwargs):
        if self.is_superuser == False:
            self.set_password(self.password)
        super().save(*args, **kwargs)


class Address(models.Model):
    """
    address model for adding user's addresses
    """

    costumer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='costumer_address')
    province = models.CharField(max_length=25)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=250)
    alley = models.CharField(max_length=250)
    house_number = models.CharField(max_length=4)
    full_address = models.TextField(max_length=250)

    def __str__(self):
        return f"{self.province} {self.city}"

class UserProfile(TimeStampMixin,LogicalDeleteMixin):
    GENDER_CHOICE = (
        ('he', 'male'),
        ('she', 'female')
    )
    first_name = models.CharField(max_length=250,null=True,blank=True)
    last_name = models.CharField(max_length=250,null=True,blank=True)
    gender = models.CharField(choices=GENDER_CHOICE, max_length=250, null=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_profile')