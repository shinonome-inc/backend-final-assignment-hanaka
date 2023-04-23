from django.conf import settings
from django.db import models
from django.urls import reverse


class Tweet(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="tweets", on_delete=models.CASCADE
    )
    content = models.TextField(verbose_name="内容", max_length=140)
    created_at = models.DateTimeField(verbose_name="作成日", auto_now_add=True)

    class Meta:
        verbose_name_plural = "ツイート"

    def __str__(self):
        return f"{self.user.username} : {self.content}"

    def get_absolute_url(self):
        return reverse("tweets:detail", kwargs={"pk": self.pk})

    # related_nameはデフォルトではモデル名(小文字)_set
    # get_absolute_url(): modelの詳細ページのURLを返すメソッド


class Like(models.Model):
    tweet = models.ForeignKey("Tweet", related_name="likes", on_delete=models.CASCADE)
    """
    ForeignKeyの第一引数は文字列で指定してもモデルクラス自体を指定してもOK。
    モデル自体で指定するためには、その前で引数に入れるモデルクラスが指定されている必要あり。
    また、他モデルとの依存関係の明確化＆可読性を考慮して、文字列で指定することが推奨されている◎
    公式ドキュメント https://docs.djangoproject.com/ja/3.2/ref/models/fields/#django.db.models.ForeignKey
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="likes", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "いいね"
        constraints = [
            models.UniqueConstraint(fields=["tweet", "user"], name="like_unique"),
        ]

    def __str__(self):
        return f"{self.tweet.content} by {self.user.username}"
