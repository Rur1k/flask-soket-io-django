import jwt

from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Имя пользователя - не может быть пустым')
        if email is None:
            raise TypeError('Email -  не может быть пустым')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Пароль - не может быть пустым')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username


class Task(models.Model):
    STATUS = (
        ('new', 'Новая'),
        ('in_work', 'В работе'),
        ('completed', 'Выполнена'),
        ('cancel', 'Отмена'),
        ('refusal', 'Отказ'),
    )
    
    id = models.AutoField(unique=True, primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator', null=True, blank=True)
    name = models.CharField('Название', max_length=64)
    description = models.TextField(null=True, blank=True)
    executor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='executor')
    status = models.CharField(max_length=16, choices=STATUS, default="new", blank=True)
