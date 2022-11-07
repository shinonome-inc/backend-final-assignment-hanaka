from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=254)
    skill = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "ユーザー"

    # https://codor.co.jp/django/how-to-use-verbose-name
    # そもそもMetaデータとは、データを分かりやすく説明するための付帯情報


# class FriendShip(models.Model):
#     pass
