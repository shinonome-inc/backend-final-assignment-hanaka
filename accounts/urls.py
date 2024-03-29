from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("<str:username>/", views.UserProfileView.as_view(), name="user_profile"),
    path("<str:username>/follow/", views.FollowView.as_view(), name="follow"),
    path("<str:username>/unfollow/", views.UnFollowView.as_view(), name="unfollow"),
    path(
        "<str:username>/following_list/",
        views.FollowingListView.as_view(),
        name="following_list",
    ),
    path(
        "<str:username>/follower_list/",
        views.FollowerListView.as_view(),
        name="follower_list",
    ),
]
# app_nameとpathの引数のnameで逆引きしていく
# .as_view()と同時に色々なメソッドが実行される。pathの中身をインスタンス化している
