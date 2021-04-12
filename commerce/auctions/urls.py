from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("test", views.test, name="test"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchtest", views.watchtest, name="watchtest"),
    path("seller", views.seller, name="seller"),
    path("<str:category>", views.category_search, name="category_search")
    
]
