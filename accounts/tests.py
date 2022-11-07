from django.conf import settings
from django.contrib.auth import SESSION_KEY
from django.test import TestCase
from django.urls import reverse

from .models import User

# print(settings.LOGIN_REDIRECT_URL)


class TestSignUpView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")  # urls.pyの(app_name:name)

    def test_success_get(self):
        response = self.client.get(self.url)  # 仮想的なHTTPリクエストを送信し、レスポンスを受け取る
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")  # templatesを指定しなくていい？

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

    """
        response = self.client.post(self.url, empty_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "username",
            "このフィールドは必須です。",
        )

        # self.assertFormsetError(formset, form_index, field, errors, msg_prefix='')
        # field and errors have the same meaning as the parameters to assertFormError().
        # https://selfs-ryo.com/detail/django_test_1

        self.assertFormError(
            response,
            "form",
            "email",
            "このフィールドは必須です。",
        )
        self.assertFormError(
            response,
            "form",
            "password1",
            "このフィールドは必須です。",
        )
        self.assertFormError(
            response,
            "form",
            "password2",
            "このフィールドは必須です。",
        )
        self.assertFalse(User.objects.exists())  # データ格納だめ
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


class TestLoginView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_empty_password(self):
        pass


class TestLogoutView(TestCase):
    def test_success_get(self):
        pass


class TestUserProfileView(TestCase):
    def test_success_get(self):
        pass


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
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_user(self):
        pass

    def test_failure_post_with_self(self):
        pass


class TestUnfollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowingListView(TestCase):
    def test_success_get(self):
        pass


class TestFollowerListView(TestCase):
    def test_success_get(self):
        pass
