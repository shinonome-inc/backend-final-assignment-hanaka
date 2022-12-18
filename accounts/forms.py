from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User

# from django.contrib.auth import get_user_model
# User = get_user_model() でも〇
# ↑CustomUserモデル、DjangoデフォルトのUserモデルを問わず、使用しているUserモデル自体を返してくれる


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )
        # UserCreationFormでpassword1/2は書かれているのでfields= に書く必要なし。


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label


# https://freeheroblog.com/forms-request/
# https://freeheroblog.com/args-kwargs/
