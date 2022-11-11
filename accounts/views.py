from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin  # , UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import LoginForm, SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("tweets:home")
    # reverse(app名:urls.pyで設定した名前)

    def form_valid(self, form):
        form.save()  # formの情報を保存
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        if user is not None:
            print(user)
            login(self.request, user)  # 認証
        return super().form_valid(form)  # リダイレクト
        # https://docs.djangoproject.com/ja/4.1/topics/auth/default/#authenticating-users


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"


class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "accounts/logout.html"
