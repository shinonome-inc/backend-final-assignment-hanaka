from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from .forms import LoginForm, SignUpForm
from .models import FriendShip, User


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("tweets:home")
    # reverse(app名:urls.pyで設定した名前)
    # クラス変数の段階ではまだurls.pyが読み込まれていないのでreverseだとエラーが出てしまう

    def form_valid(self, form):
        response = super().form_valid(form)
        # ↑ valid を通ったので ↓ cleaned_data というデータ(dict型)に格納される
        username = form.cleaned_data.get("username")
        # わざわざgetにしなくても、username = form.cleaned_data["username"]でキー指定すれば良かったっぽい
        password = form.cleaned_data.get("password1")  # passwordというフォームはないので注意
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)  # 認証バックエンド
        return response  # リダイレクト
        # https://docs.djangoproject.com/ja/4.1/topics/auth/default/#authenticating-users
        # この関数の中でデータをDBに登録する＆success_urlにリダイレクトさせる

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

    def get_context_data(self, **kwargs):
        # Insert the single object into the context dict.
        context = super().get_context_data(**kwargs)
        # 既存のコンテキストデータを取得
        # ↓↓ 追加したい情報たち
        user = self.object
        context["tweet_list"] = user.tweet_set.order_by("-created_at")
        # User＆Tweetテーブルを合体させる(INNER JOIN)
        # オブジェクト名.モデル名(小文字)_set.クエリセットAPI：1対多 の参照。
        context["is_following"] = FriendShip.objects.filter(
            following=user, follower=self.request.user
        ).exists()
        # exists() : boolの代わりに、少なくともひとつ以上の結果があるか判断するクエリセットAPI(なくても行けそう)
        # 参考：https://man.plustar.jp/django/ref/models/querysets.html#django.db.models.query.QuerySet.exists
        context["following_count"] = FriendShip.objects.filter(follower=user).count()
        context["follower_count"] = FriendShip.objects.filter(following=user).count()
        user = self.request.user  # userという変数を上書きしてしまうのはOKなのか...？
        context["liked_list"] = user.like_set.values_list("tweet", flat=True)
        return context


class FollowView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        follower = self.request.user  # ログイン中のユーザーを参照
        following = get_object_or_404(User, username=self.kwargs["username"])

        if follower == following:
            # = : 代入
            # == : 比較演算子
            messages.warning(request, "無効な操作です。")
            return render(request, "tweets/home.html")
        elif FriendShip.objects.filter(follower=follower, following=following).exists():
            messages.warning(request, f"あなたはすでに { following.username } をフォローしています。")
            return render(request, "tweets/home.html")
        else:
            FriendShip.objects.create(follower=follower, following=following)
            messages.info(request, f"{ following.username } をフォローしました。")
            return redirect("tweets:home")


class UnFollowView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        follower = self.request.user
        following = get_object_or_404(User, username=self.kwargs["username"])

        if friend := FriendShip.objects.filter(following=following, follower=follower):
            friend.delete()
            messages.info(request, f"{following.username} のフォローを解除しました。")
            return redirect("tweets:home")
        else:
            messages.warning(request, "無効な操作です。")
            return render(request, "tweets/home.html")
        # セイウチ演算子：代入文 → 代入式として使えるように！！
        # 特にif文においては、代入と評価を同時に行うことが出来るようになる。


class FollowingListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "accounts/following_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs["username"])
        context["following_list"] = FriendShip.objects.select_related(
            "following"
        ).filter(follower=user)
        # select_related：User＆FriendShipテーブルを合体させる(INNER JOIN)
        return context


class FollowerListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "accounts/follower_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs["username"])
        # urlで表示している人の情報を持ってくる
        context["follower_list"] = FriendShip.objects.select_related("follower").filter(
            following=user
        )
        return context
