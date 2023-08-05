from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    profile_image=models.ImageField(default='users/images/user-default.png',upload_to='users/images/')
