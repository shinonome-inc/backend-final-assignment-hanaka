from django.conf import settings
from django.contrib.auth import SESSION_KEY
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from tweets.models import Tweet

from .models import FriendShip, User


class TestSignUpView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")  # urls.pyの(app_name:name)

    def test_success_get(self):
        response = self.client.get(self.url)  # 仮想的なHTTPリクエストを送信し、レスポンスを受け取る
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_success_post(self):
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, user_data)
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )  # リダイレクト

        self.assertTrue(
            User.objects.filter(
                username=user_data["username"],
                email=user_data["email"],
            ).exists()
        )  # DBのレコードが追加されていて、入力データと同一

        self.assertIn(SESSION_KEY, self.client.session)
        # ログイン後のサーバー上のsession_key＝ブラウザ上のkeyの確認(clientがテスト内でwebブラウザとして機能する)。

    def test_failure_post_with_empty_form(self):
        empty_data = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }

        response = self.client.post(self.url, data=empty_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)

        context = response.context
        form = context["form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["username"][0], "このフィールドは必須です。")
        self.assertEqual(form.errors["email"][0], "このフィールドは必須です。")
        self.assertEqual(form.errors["password1"][0], "このフィールドは必須です。")
        self.assertEqual(form.errors["password2"][0], "このフィールドは必須です。")
        # assertIs(form.errors["username"][0],"このフィールドは必須です。")だと通らなかった
        """
         ↑↑↑
         print(id(form.errors["username"][0]))
         print(id("このフィールドは必須です。"))
        ここふたつ発行されているidが違う➤全く同じオブジェクトではない➤Isだと通らない
        """

    def test_failure_post_with_empty_username(self):
        username_empty_data = {
            "username": "",
            "email": "testmail@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, data=username_empty_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)

        context = response.context
        form = context["form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["username"][0], "このフィールドは必須です。")
        # formの引用元　×SignUpForm(username_empty_data)
        # https://codor.co.jp/django/about-context

    def test_failure_post_with_empty_email(self):
        email_empty_data = {
            "username": "testuser",
            "email": "",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, data=email_empty_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)

        context = response.context
        form = context["form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"][0], "このフィールドは必須です。")

    def test_failure_post_with_empty_password(self):
        password_empty_data = {
            "username": "testuser",
            "email": "testmail@example.com",
            "password1": "",
            "password2": "",
        }

        response = self.client.post(self.url, data=password_empty_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)

        context = response.context
        form = context["form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password1"][0], "このフィールドは必須です。")
        self.assertEqual(form.errors["password2"][0], "このフィールドは必須です。")

    def test_failure_post_with_duplicated_user(self):
        duplicated_data = {
            "username": "testuser",
            "email": "testmail@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        User.objects.create_user(
            username="testuser",
            email="testemail@example.com",
            password="testpassword",
        )

        response = self.client.post(self.url, data=duplicated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 1)

        context = response.context
        form = context["form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["username"][0], "同じユーザー名が既に登録済みです。")

    def test_failure_post_with_invalid_email(self):
        invalid_email_data = {
            "username": "testuser",
            "email": "test",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, data=invalid_email_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)

        context = response.context
        form = context["form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"][0], "有効なメールアドレスを入力してください。")

    def test_failure_post_with_too_short_password(self):
        short_password_data = {
            "username": "testuser",
            "email": "testmail@example.com",
            "password1": "short",
            "password2": "short",
        }

        response = self.client.post(self.url, data=short_password_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)

        context = response.context
        form = context["form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password2"][0], "このパスワードは短すぎます。最低 8 文字以上必要です。")

    def test_failure_post_with_password_similar_to_username(self):
        password_similar_to_username_data = {
            "username": "testuser",
            "email": "testmail@example.com",
            "password1": "testuserr",
            "password2": "testuserr",
        }

        response = self.client.post(self.url, data=password_similar_to_username_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)

        context = response.context
        form = context["form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password2"][0], "このパスワードは ユーザー名 と似すぎています。")

    def test_failure_post_with_only_numbers_password(self):
        only_numbers_password_data = {
            "username": "testuser",
            "email": "testmail@example.com",
            "password1": "84927274",
            "password2": "84927274",
        }

        response = self.client.post(self.url, data=only_numbers_password_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)

        context = response.context
        form = context["form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password2"][0], "このパスワードは数字しか使われていません。")

    def test_failure_post_with_mismatch_password(self):
        mismatch_password_data = {
            "username": "testuser",
            "email": "testmail@example.com",
            "password1": "firstpassword",
            "password2": "secondpassword",
        }

        response = self.client.post(self.url, data=mismatch_password_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)

        context = response.context
        form = context["form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password2"][0], "確認用パスワードが一致しません。")


class TestLoginView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testemail@example.com",
            password="testpassword",
        )
        self.url = reverse("accounts:login")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_success_post(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(
            response,  # GET/POSTしたレスポンス
            reverse(settings.LOGIN_REDIRECT_URL),  # 最終的にリダイレクトされるURL
            status_code=302,  # はじめに返ってくるHTTPのレスポンスコード
            target_status_code=200,  # 最終的に返ってくるHTTPのレスポンスコード
        )  # https://qiita.com/kozakura16/items/c08b8cb8da12ace78658

        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_not_exists_user(self):
        not_exist_user_data = {
            "username": "fakeuser",
            "password": "fakepassward",
        }
        response = self.client.post(self.url, not_exist_user_data)
        self.assertEqual(response.status_code, 200)
        context = response.context
        form = context["form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["__all__"][0],
            "正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。",
        )
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_password(self):
        empty_data = {
            "username": "testuser",
            "password": "",
        }
        response = self.client.post(self.url, empty_data)
        self.assertEqual(response.status_code, 200)
        context = response.context
        form = context["form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password"][0], "このフィールドは必須です。")
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestLogoutView(TestCase):
    def setUp(self):
        self.usr = User.objects.create_user(
            username="testuser",
            password="password",
        )
        self.client.login(username="testuser", password="password")

    def test_success_get(self):
        response = self.client.get(reverse("accounts:logout"))
        self.assertRedirects(
            response,
            reverse(settings.LOGOUT_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestUserProfileView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1",
            password="testpassword",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="testpassword",
        )
        self.client.login(username="testuser1", password="testpassword")
        self.post = Tweet.objects.create(user=self.user1, content="testpost")
        self.url = reverse(
            "accounts:user_profile", kwargs={"username": self.user1.username}
        )
        self.friendship = FriendShip.objects.create(
            follower=self.user1, following=self.user2
        )

    def test_success_get(self):
        response = self.client.get(self.url)
        context = response.context
        self.assertQuerysetEqual(
            context["tweet_list"], Tweet.objects.filter(user=self.user1)
        )
        self.assertEqual(
            context["following_count"],
            FriendShip.objects.filter(follower=self.user1).count(),
        )
        self.assertEqual(
            context["follower_count"],
            FriendShip.objects.filter(following=self.user1).count(),
        )
        # usernameを元に情報を取ってきている


class TestUserProfileEditView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowView(TestCase):
    def setUp(self):

        self.user1 = User.objects.create_user(
            username="testuser1",
            password="testpassword",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="testpassword",
        )
        self.client.login(username="testuser1", password="testpassword")

    def test_success_post(self):
        url = reverse("accounts:follow", kwargs={"username": self.user2.username})
        response = self.client.post(url)
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(
            FriendShip.objects.filter(
                follower=self.user1, following=self.user2
            ).exists()
        )

    def test_failure_post_with_not_exist_user(self):
        url = reverse("accounts:follow", kwargs={"username": "not_exist_username"})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(
            FriendShip.objects.filter(
                follower=self.user1, following__username="not_exist_username"
            ).exists()
        )

    def test_failure_post_with_self(self):
        url = reverse("accounts:follow", kwargs={"username": self.user1.username})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        message = str(messages[0])
        self.assertEquals(message, "無効な操作です。")
        self.assertFalse(
            FriendShip.objects.filter(
                following=self.user1, follower=self.user1
            ).exists()
        )


class TestUnfollowView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1",
            password="testpassword",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="testpassword",
        )
        self.client.login(username="testuser1", password="testpassword")
        FriendShip.objects.create(follower=self.user1, following=self.user2)

    def test_success_post(self):
        url = reverse("accounts:unfollow", kwargs={"username": self.user2.username})
        response = self.client.post(url)
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertFalse(
            FriendShip.objects.filter(
                follower=self.user1, following=self.user2
            ).exists()
        )

    def test_failure_post_with_not_exist_user(self):
        url = reverse("accounts:unfollow", kwargs={"username": "not_exist_username"})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            FriendShip.objects.filter(
                follower=self.user1, following=self.user2
            ).exists()
        )

    def test_failure_post_with_incorrect_user(self):
        url = reverse("accounts:unfollow", kwargs={"username": self.user1.username})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        message = str(messages[0])
        self.assertEquals(message, "無効な操作です。")
        self.assertTrue(
            FriendShip.objects.filter(
                follower=self.user1, following=self.user2
            ).exists()
        )


class TestFollowingListView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.login(username="testuser", password="testpassword")

    def test_success_get(self):
        url = reverse(
            "accounts:following_list", kwargs={"username": self.user.username}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/following_list.html")


class TestFollowerListView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.login(username="testuser", password="testpassword")

    def test_success_get(self):
        url = reverse("accounts:follower_list", kwargs={"username": self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/follower_list.html")
