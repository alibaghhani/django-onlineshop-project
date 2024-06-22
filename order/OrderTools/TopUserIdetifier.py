from abc import ABC, abstractmethod

from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from account.models import User, UserProfile
from config import settings
from order.models import OrderItem
from product.models import DiscountCode
import logging

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



