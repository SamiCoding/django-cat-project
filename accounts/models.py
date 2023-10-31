from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

class User(AbstractUser):
    username = models.CharField(
        error_messages={'unique': 'A user with that username already exists.'},
        help_text='Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only.',
        max_length=20,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        verbose_name='username',
    )
