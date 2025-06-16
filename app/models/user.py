from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    GENDERS = [
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    ]
    gender=models.CharField(max_length=1, choices=GENDERS)

    def __str__(self):
        return self.username
