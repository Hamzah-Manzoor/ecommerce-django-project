from django.db import models
from users.models import User


class Shop(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Shop Owner'})
    name = models.CharField(max_length=255, unique=True)
    location = models.TextField()
    contact_number = models.CharField(max_length=15)


class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
