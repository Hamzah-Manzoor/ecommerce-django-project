from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser, models.Model):
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
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True,
                                        default='profile_pics/default.png')

