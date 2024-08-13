from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Order, Payment
from decimal import Decimal


@receiver(pre_save, sender=Order)
def pre_save_order(sender, instance, **kwargs):

    if isinstance(instance.total_amount, str):
        instance.total_amount = Decimal(instance.total_amount)  # Converting the string to a Decimal

    instance.total_amount *= Decimal('1.17')  # Adding a 17% tax on the total amount
    print("--------------------------------")
    print("This is pre_save_order.")
    print("--------------------------------")


@receiver(post_save, sender=Order)
def post_save_order(sender, instance, created, **kwargs):
    if created:
        print("--------------------------------")
        print("This is post_save_order.")
        print("--------------------------------")
