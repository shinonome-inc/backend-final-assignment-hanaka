# from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import User

# User = get_user_model()


class SignUpForm(UserCreationForm):
    User._meta.get_field("email").required = True

    class Meta:
        model = User
        fields = ("username", "email")
