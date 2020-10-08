from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:listing_id>", views.listing_view, name="listing_view"),
    path("bid", views.bid, name='bid'),
    path("comment", views.comment, name='comment'),
    path("categories", views.categories_view, name="categories_view"),
    path("<str:category>", views.category_view, name="category_view"),
    path("close/", views.close_auction, name='close_auction'),
    path("watchlist/", views.watchlist, name='watchlist'),
    path("watchlist/<int:user_id>", views.watchlist_view, name='watchlist_view')
]
