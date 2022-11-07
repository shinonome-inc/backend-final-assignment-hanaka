from django.test import TestCase
from django.urls import reverse


class TestHomeView(TestCase):
    def setUp(self):
        self.url = reverse("tweets:home")  # urls.pyの(app_name:name)

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/home.html")


class TestTweetCreateView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_empty_content(self):
        pass

    def test_failure_post_with_too_long_content(self):
        pass


class TestTweetDetailView(TestCase):
    def test_success_get(self):
        pass


class TestTweetDeleteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


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
