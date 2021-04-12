from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("ouda", views.ouda, name="ouda"),
    path("brian", views.brian, name="brian"),
    path("<str:name>", views.greet, name="greet")
]