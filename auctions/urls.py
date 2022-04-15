from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<str:item_name>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories/<str:cat_name>", views.categories, name="categories")
]
