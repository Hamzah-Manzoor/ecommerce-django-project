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


class RequestLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=200)
    status_code = models.IntegerField()
    duration = models.FloatField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} {self.path} {self.status_code}"

