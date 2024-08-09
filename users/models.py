from django.db import models


class User(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Shop Owner', 'Shop Owner'),
        ('Customer', 'Customer'),
    ]

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
