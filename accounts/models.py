from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
   phone = models.CharField(max_length=15, null=True, blank=True)
   account_number = models.CharField(max_length=20, null=True, blank=True)
   bank_name = models.CharField(max_length=100, null=True, blank=True)
   account_name = models.CharField(max_length=150, null=True, blank=True)

   def __str__(self):
        return self.username