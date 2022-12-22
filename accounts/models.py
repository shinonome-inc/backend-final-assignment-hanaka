from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=254)
    # emailのbrank=trueになっているのを上書きするために記述
    # EmailFieldを使うことで@が必要とかバリデーション関連を追加する

    class Meta:
        verbose_name_plural = "ユーザー"

    def __str__(self):
        return self.username

    # adminサイトでusernameを表示する(デフォルトでusernameになっているので本当は特に記述の必要なし)

    # https://codor.co.jp/django/how-to-use-verbose-name
    # そもそもMetaデータとは、データを分かりやすく説明するための付帯情報


class FriendShip(models.Model):
    follower = models.ForeignKey(
        User,
        related_name="follower",
        on_delete=models.CASCADE,
    )
    following = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "フォロー/フォロワー"
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"], name="friendship_unique"
            ),
        ]
