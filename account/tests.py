from django.core.exceptions import ValidationError
from django.test import TestCase

from account.models import User  # Replace 'your_app_name' with the actual name of your Django app
from .models import Address, UserProfile


class UserModelTestCase(TestCase):
    """
    user model testcase
    """

    def test_valid_email(self):
        user = User.objects.create(
            first_name='John',
            last_name='Doe',
            email='johndoe@gmail.com'
        )

        try:
            user.full_clean()
        except ValidationError as e:
            self.fail(f"ValidationError raised: {e.message}")

    def test_invalid_email(self):
        with self.assertRaises(ValidationError) as context:
            user = User.objects.create(
                first_name='John',
                last_name='Doe',
                email='baghaniali2006@gmail.com'
            )
            user.full_clean()

        self.assertEqual(
            context.exception.messages[0],
            'لطفا یک ایمیل درست وارد کنید'
        )


class AddressModelTestCase(TestCase):
    """
    address model testcase
    """

    def setUp(self):
        self.user = User.objects.create(email='test@gmail.com', admin_name='admin', is_superuser=False, is_staff=False)

    def test_address_creation(self):
        address = Address.objects.create(costumer=self.user, province='Province', city='City', street='Street',
                                         alley='Alley', house_number='123', full_address='Full Address')
        self.assertTrue(isinstance(address, Address))
        self.assertEqual(address.costumer, self.user)
        self.assertEqual(address.province, 'Province')
        self.assertEqual(address.city, 'City')
        self.assertEqual(address.street, 'Street')
        self.assertEqual(address.alley, 'Alley')
        self.assertEqual(address.house_number, '123')
        self.assertEqual(address.full_address, 'Full Address')


class UserProfileModelTestCase(TestCase):
    """
    profile model testcase
    """

    def setUp(self):
        self.user = User.objects.create(email='test@gmail.com', admin_name='admin', is_superuser=False, is_staff=False)

    def test_user_profile_creation(self):
        user_profile = UserProfile.objects.create(user=self.user, first_name='John', last_name='Doe', gender='he')
        self.assertTrue(isinstance(user_profile, UserProfile))
        self.assertEqual(user_profile.user, self.user)
        self.assertEqual(user_profile.first_name, 'John')
        self.assertEqual(user_profile.last_name, 'Doe')
        self.assertEqual(user_profile.gender, 'he')
