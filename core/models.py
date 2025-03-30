from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass
    # email = models.EmailField(unique=True)
