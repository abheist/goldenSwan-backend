from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.CharField(max_length=500, blank=True)
    dob = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    facebook = models.CharField(max_length=128, blank=True)
    twitter = models.CharField(max_length=128, blank=True)
    instagram = models.CharField(max_length=128, blank=True)
    linkedin = models.CharField(max_length=128, blank=True)
