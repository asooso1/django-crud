from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
# Create your models here.

class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name='followings')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)