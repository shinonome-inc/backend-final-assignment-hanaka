# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from .forms import CreateTweetForm
from .models import Like, Tweet


class HomeView(LoginRequiredMixin, ListView):
    model = Tweet
    template_name = "tweets/home.html"
    context_object_name = "tweet_list"
    # テンプレートで表示する際のモデルの参照名を設定
    # → どこから持ってきたデータか分かり易くなった気がする
    queryset = Tweet.objects.select_related("user").order_by("-created_at")
    # created_at を、マイナスを付けることで日付が新しい順にしてる

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["liked_list"] = user.like_set.values_list("tweet", flat=True)
        # ログイン中のユーザーがいいねしているツイート一覧をidで取得
        return context


class TweetCreateView(LoginRequiredMixin, CreateView):
    form_class = CreateTweetForm
    template_name = "tweets/tweet_create.html"
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        # formでログインユーザーを取得する
        return super().form_valid(form)
        # super(): classの継承元の何かを呼び出す時に用いる(今回で言うとCreateView)


class TweetDetailView(LoginRequiredMixin, DetailView):
    model = Tweet
    context_object_name = "tweet_detail"
    template_name = "tweets/tweet_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["like_count"] = Like.objects.filter(tweet=self.object).count()
        return context


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    template_name = "tweets/tweet_delete.html"
    success_url = reverse_lazy("tweets:home")
    context_object_name = "tweet_delete"

    def test_func(self):
        tweet = self.get_object()
        return self.request.user == tweet.user


class LikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        tweet_id = self.kwargs["pk"]
        tweet = get_object_or_404(Tweet, id=tweet_id)
        Like.objects.get_or_create(tweet=tweet, user=user)
        is_liked = True
        url = reverse("tweets:unlike", kwargs={"pk": tweet_id})
        context = {"is_liked": is_liked, "url": url}
        return JsonResponse(context)


class UnlikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        tweet_id = self.kwargs["pk"]
        tweet = get_object_or_404(Tweet, id=tweet_id)
        if like := Like.objects.filter(user=user, tweet=tweet):
            like.delete()
        is_liked = False
        url = reverse("tweets:like", kwargs={"pk": tweet_id})
        context = {"is_liked": is_liked, "url": url}
        return JsonResponse(context)
