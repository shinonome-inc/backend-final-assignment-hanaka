from django.test import TestCase
from django.urls import reverse

from accounts.models import User

from .models import Tweet


class TestHomeView(TestCase):
    def setUp(self):
        self.url = reverse("tweets:home")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.login(username="testuser", password="testpassword")
        # self.client.post(reverse("accounts:signup"), self.user)にする手もある。
        self.post = Tweet.objects.create(user=self.user, content="testpost")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/home.html")
        context = response.context
        self.assertQuerysetEqual(
            context["tweet_list"], Tweet.objects.all(), ordered=False
        )
        # QSが特定の値のリストを返すことを保証するテスト
        # https://docs.djangoproject.com/ja/3.1/topics/testing/tools/#django.test.TransactionTestCase.assertQuerysetEqual


class TestTweetCreateView(TestCase):
    def setUp(self):
        self.url = reverse("tweets:create")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.login(username="testuser", password="testpassword")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/tweet_create.html")

    def test_success_post(self):
        test_post = {
            "content": "testpost",
        }

        response = self.client.post(self.url, test_post)
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertEqual(Tweet.objects.count(), 1)  # いるのかな
        self.assertTrue(Tweet.objects.filter(content=test_post["content"]).exists())

    def test_failure_post_with_empty_content(self):
        empty_content_post = {
            "content": "",
        }

        response = self.client.post(self.url, empty_content_post)
        self.assertEqual(response.status_code, 200)
        context = response.context
        form = context["form"]
        self.assertEqual(Tweet.objects.count(), 0)
        self.assertEqual(
            form.errors["content"][0],
            "このフィールドは必須です。",
        )

    def test_failure_post_with_too_long_content(self):
        too_long_content_data = {
            "content": "a" * 183,
        }
        response = self.client.post(self.url, too_long_content_data)
        context = response.context
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            context["form"].errors["content"][0],
            "この値は 140 文字以下でなければなりません( 183 文字になっています)。",
        )
        self.assertEqual(Tweet.objects.count(), 0)


class TestTweetDetailView(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.login(username="testuser", password="testpassword")
        self.post = Tweet.objects.create(user=self.user, content="testpost")
        self.url = reverse("tweets:detail", kwargs={"pk": self.post.pk})

    def test_success_get(self):
        response = self.client.get(self.url)
        context = response.context
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            context["tweet_detail"],
            self.post,
        )
        # getのテストでpostの内容を見たいときは、setUpの時にデータを作っておいてあげればいい


class TestTweetDeleteView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1",
            password="testpassword1",
        )

        self.client.login(username="testuser1", password="testpassword1")
        self.post = Tweet.objects.create(user=self.user1, content="testpost1")

    def test_success_post(self):
        self.url = reverse("tweets:delete", kwargs={"pk": self.post.pk})
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertEqual(Tweet.objects.count(), 0)

    def test_failure_post_with_not_exist_tweet(self):
        self.url = reverse("tweets:delete", kwargs={"pk": 10})
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.context["exception"],
            "クエリーに一致する tweet は見つかりませんでした",
        )
        self.assertEqual(Tweet.objects.count(), 1)

    def test_failure_post_with_incorrect_user(self):
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="testpassword2",
        )
        self.post2 = Tweet.objects.create(user=self.user2, content="testpost2")
        self.url = reverse("tweets:delete", kwargs={"pk": self.post2.pk})
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)
        # エラーメッセージの確認入れる?
        self.assertEqual(Tweet.objects.count(), 2)


class TestFavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_favorited_tweet(self):
        pass


class TestUnfavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_unfavorited_tweet(self):
        pass
