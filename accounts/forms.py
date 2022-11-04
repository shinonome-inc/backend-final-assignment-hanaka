from django.contrib.auth.forms import UserCreationForm

from .models import User

# from django.contrib.auth import get_user_model
# User = get_user_model() でも〇


class SignUpForm(UserCreationForm):
    User._meta.get_field("email").required = True

    class Meta:
        model = User
        fields = ("username", "email")
