from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=254)

    class Meta:
        verbose_name_plural = "ユーザー"

    # https://codor.co.jp/django/how-to-use-verbose-name
    # そもそもMetaデータとは、データを分かりやすく説明するための付帯情報


# class FriendShip(models.Model):
#     pass
