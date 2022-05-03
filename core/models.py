from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have a valid e-mail address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class Payer(models.Model):
    company = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.company


class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        related_name='transaction',
        on_delete=models.CASCADE
    )
    payer = models.ForeignKey(
        Payer,
        related_name='transaction',
        on_delete=models.RESTRICT
    )
    points = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)