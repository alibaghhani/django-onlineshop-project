import logging
from abc import ABC, abstractmethod

from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from account.models import User, UserProfile
from config import settings
from order.models import OrderItem
from product.models import DiscountCode

logging.basicConfig(level=logging.INFO, filename="order/logs/order_logs.log", filemode="a")


class TopUsersFactory(ABC):

    @abstractmethod
    def generate_discount_token(self, user):
        pass

    @abstractmethod
    def check_is_paid_orders(self, user):
        pass

    @abstractmethod
    def calculate_final_amount(self, payments: dict):
        pass

    @abstractmethod
    def user_type(self, user, amount: int):
        pass

    @abstractmethod
    def send_notification(self, user, token):
        pass


class BrilliantUsers(TopUsersFactory):
    def __init__(self):
        logging.info("entered into BrilliantUsers class")

    def generate_discount_token(self, user):
        code = get_random_string(length=5)
        discount = 70
        user = user
        DiscountCode.objects.create(
            code=code,
            discount=discount,
            type_of_discount='percentage',
            user_id=user.id
        )
        return code

    def check_is_paid_orders(self, user):
        logging.info('Checking paid orders for BrilliantUsers')
        user_payments = {}
        order_items = OrderItem.objects.filter(order__customer_id=user, order__is_paid=True)
        logging.info(order_items)
        for item in order_items:
            if item.id not in user_payments:
                user_payments[item.id] = item.price
        return user_payments

    def calculate_final_amount(self, payments: dict):
        logging.info('Calculating final amount for BrilliantUsers')
        return sum(payments.values())

    def user_type(self, user, amount: int):
        logging.info(f'Determining user type for BrilliantUsers: user={user}, amount={amount}')
        logging.info(type(amount))
        if amount >= 500000:
            logging.info('entered into if statement')
            profile = UserProfile.objects.get(user_id=user)
            logging.info(f'user type: {profile.type}')
            profile.type = 'Brilliant'
            profile.save()
            logging.info(f'New user type: {profile.type}')
            self.generate_discount_token(user)
            return profile.type

    def send_notification(self, user: User, token: str):
        logging.info(f'Sending notification to {user.username} (BrilliantUsers)')
        subject = f'congratulations {user.username}'
        message = (f"you have reached 500000 order amount "
                   f"here's your discount coupon {token} "
                   "you are now a Brilliant user")

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, email_from, recipient_list)


class GoldUsers(TopUsersFactory):
    def __init__(self):
        logging.info('we are now on gold user')

    def generate_discount_token(self, user):
        code = get_random_string(length=5)
        discount = 50
        user = user
        DiscountCode.objects.create(
            code=code,
            discount=discount,
            type_of_discount='percentage',
            user_id=user.id
        )
        return code

    def check_is_paid_orders(self, user):
        logging.info('Checking paid orders for GoldUsers')
        user_payments = {}
        order_items = OrderItem.objects.filter(order__customer_id=user, order__is_paid=True)
        for item in order_items:
            if item.id not in user_payments:
                user_payments[item.id] = item.price
        return user_payments

    def calculate_final_amount(self, payments: dict):
        logging.info('Calculating final amount for GoldUsers')
        return sum(payments.values())

    def user_type(self, user, amount: int):
        logging.info(f'Determining user type for GoldUsers: user={user}, amount={amount}')
        if 100000 <= amount < 500000:
            profile = UserProfile.objects.get(user_id=user)
            logging.info(f'Old user type: {profile.type}')
            profile.type = 'Gold'
            profile.save()
            logging.info(f'New user type: {profile.type}')
            self.generate_discount_token(user)
            return profile.type

    def send_notification(self, user: User, token: str):
        logging.info(f'Sending notification to {user.username} (GoldUsers)')
        subject = f'congratulations {user.username}'
        message = ("you have reached 100000 order amount "
                   f"here's your discount coupon {token} "
                   "you are now a Gold user")

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, email_from, recipient_list)


