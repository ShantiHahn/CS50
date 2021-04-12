from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search_page/", views.search_page, name="search_page"),
    path("<str:title>", views.get_page, name="get_page"),
    path("random_page/", views.random_page, name="random_page"),
    path("edit/<str:title>", views.edit_content, name="edit_content"),
    path("new_page/", views.new_page, name="new_page")
]
