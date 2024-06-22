import logging

from celery import shared_task

from account.models import User
from order.OrderTools.Checker import UsersOrderChecker
from order.OrderTools.TopUserIdetifier import (BrilliantUsers, BronzeUsers,
                                               GoldUsers, SilverUsers)

brilliant_top_users = BrilliantUsers()
gold_top_users = GoldUsers()
silver_top_users = SilverUsers()
bronze_top_users = BronzeUsers()

brilliant_checker = UsersOrderChecker(bronze_top_users)
gold_checker = UsersOrderChecker(gold_top_users)
silver_checker = UsersOrderChecker(silver_top_users)
bronze_checker = UsersOrderChecker(bronze_top_users)


@shared_task
def get_users():
    users = User.objects.all()
    for customer in users:
        logging.info(f'Checking customer {customer.email}')
        for checker in [brilliant_checker, gold_checker, silver_checker, bronze_checker]:
            checker.identify_user(customer)
