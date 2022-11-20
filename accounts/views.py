from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from tweets.models import Tweet

from .forms import LoginForm, SignUpForm
from .models import User


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("tweets:home")
    # reverse(app名:urls.pyで設定した名前)

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)  # 認証
        return response  # リダイレクト
        # https://docs.djangoproject.com/ja/4.1/topics/auth/default/#authenticating-users

    """
    ↓実際のコード引用
    def form_valid(self, form):
    ""If the form is valid, save the associated model.""
    self.object = form.save()  ※formの情報を保存
    return super().form_valid(form)
    ※データの加工は、validしたあとに行う
    """


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"


class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "accounts/logout.html"


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = "user"
    template_name = "accounts/profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    # ここでは、ユーザーが存在しなかったら404を出す処理をしたい

    def get_context_data(self, **kwargs):
        # Insert the single object into the context dict.
        context = super().get_context_data(**kwargs)
        # 既存のコンテキストデータを取得
        context["tweets"] = (
            Tweet.objects.select_related("user")
            .filter(user=self.request.user)
            .order_by("-created_at")
        )
        # 追加したい情報
        return context
