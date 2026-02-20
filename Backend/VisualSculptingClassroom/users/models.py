from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    role = (
        ('student', "Ученик"),
        ('teacher', "Преподаватель")
    )
    roles = models.CharField(max_length=20, choices=role, default="student")
