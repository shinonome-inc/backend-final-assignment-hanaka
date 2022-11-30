# modelを作成したら必ずmakemigration → python manage.py migrate する
from django.db import models
from django.urls import reverse

from accounts.models import User


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="内容", max_length=140)
    created_at = models.DateTimeField(verbose_name="作成日", auto_now_add=True)

    class Meta:
        verbose_name_plural = "Tweet"

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("tweets:detail", kwargs={"pk": self.pk})

    # get_absolute_url(): modelの詳細ページのURLを返すメソッド
