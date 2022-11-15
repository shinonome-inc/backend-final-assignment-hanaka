from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User

# from django.contrib.auth import get_user_model
# User = get_user_model() でも〇
# ↑CustomUserモデル、DjangoデフォルトのUserモデルを問わず、使用しているUserモデル自体を返してくれる


class SignUpForm(UserCreationForm):
    # User._meta.get_field("email").required = True

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label


# https://freeheroblog.com/forms-request/
# https://freeheroblog.com/args-kwargs/
