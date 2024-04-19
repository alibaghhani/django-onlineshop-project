from django.test import TestCase
from django.core.exceptions import ValidationError
from account.models import User  # Replace 'your_app_name' with the actual name of your Django app

class UserModelTestCase(TestCase):

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