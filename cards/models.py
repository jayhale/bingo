from django.conf import settings
from django.db import models

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Card(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, ondelete=models.CASCADE)
    order = models.CharField(max_length=128)

    def __str__(self):
        return str(self.user)


class Week(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Square(models.Model):
    week = models.ForeignKey(Week)
    content = models.CharField(max_length=254)

    def __str__(self):
        return self.content