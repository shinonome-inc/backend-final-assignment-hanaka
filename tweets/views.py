# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from .forms import CreateTweetForm
from .models import Tweet


class HomeView(LoginRequiredMixin, ListView):
    model = Tweet
    template_name = "tweets/home.html"
    context_object_name = "tweet_list"
    # テンプレートで表示する際のモデルの参照名を設定
    # → どこから持ってきたデータか分かり易くなった気がする
    queryset = Tweet.objects.select_related("user").order_by("-created_at")
    # created_at を、マイナスを付けることで日付が新しい順にしてる


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


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    template_name = "tweets/tweet_delete.html"
    success_url = reverse_lazy("tweets:home")
    context_object_name = "tweet_delete"

    def test_func(self):
        tweet = self.get_object()
        return self.request.user == tweet.user
