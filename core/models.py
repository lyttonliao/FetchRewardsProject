from django.db import models
from datetime import datetime


class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    points = models.PositiveIntegerField(default=0)

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
    timestamp = models.DateTimeField(default=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))