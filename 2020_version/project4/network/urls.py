
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.compose, name="compose"),
    path("posts/<int:post_id>", views.compose, name="compose"),
    path("posts/all_posts", views.all_posts, name="all_posts"),
    path("posts/follow/<str:user_name>", views.follow, name="follow"),
    path("posts/following", views.following_posts, name="following_posts"),
    path("posts/follows/<str:user_name>", views.follows, name="follows"),
    path("posts/<str:user_name>", views.profile_posts, name="profile"),
    path("posts/like/<str:post_id>", views.like, name="like")
]
