from django.contrib.auth import SESSION_KEY
from django.test import TestCase
from django.urls import reverse

from mysite import settings

from .models import User


class TestSignUpView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")  # urls.pyの(app_name:name)

    def test_success_get(self):
        response = self.client.get(self.url)  # ?
        self.assertEquals(response.status_code, 200)
        self.assertFalse(User.objects.exists())  # ?
        self.assertTemplateUsed(response, "accounts/signup.html")  # templatesを指定しなくていい？

    def test_success_post(self):
        pass

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
        )

        self.assertTrue(
            User.objects.filter(
                username=user_data["username"],
                email=user_data["email"],
            ).exists()
        )

        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_form(self):
        empty_data = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }

        response = self.client.post(self.url, empty_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "username",
            "このフィールドは必須です。",
        )
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
        self.assertFalse(User.objects.exists())

    def test_failure_post_with_empty_username(self):
        pass

    def test_failure_post_with_empty_email(self):
        pass

    def test_failure_post_with_empty_password(self):
        pass

    def test_failure_post_with_duplicated_user(self):
        pass

    def test_failure_post_with_invalid_email(self):
        pass

    def test_failure_post_with_too_short_password(self):
        pass

    def test_failure_post_with_password_similar_to_username(self):
        pass

    def test_failure_post_with_only_numbers_password(self):
        pass

    def test_failure_post_with_mismatch_password(self):
        pass


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
