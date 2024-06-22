import logging

from account.models import User
from order.OrderTools.TopUserIdetifier import (BrilliantUsers, BronzeUsers,
                                               GoldUsers, SilverUsers,
                                               TopUsersFactory)

logging.basicConfig(level=logging.INFO, filename="order/logs/order_logs.log", filemode="a")


class UsersOrderChecker:
    def __init__(self, plan: TopUsersFactory):
        self.plan = plan

    def identify_user(self, user):
        self.plan.check_is_paid_orders(user)
        calculated_amount = self.plan.check_is_paid_orders(user)
        final_amount = self.plan.calculate_final_amount(calculated_amount)
        self.plan.user_type(user, final_amount)
        self.plan.send_notification(user, token=self.plan.generate_discount_token(user))


