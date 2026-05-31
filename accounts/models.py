from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICES = (
        ('retailer', 'Retailer'),
        ('wholesaler', 'Wholesaler'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    company_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username