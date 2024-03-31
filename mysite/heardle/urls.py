from django.urls import path

from . import views

app_name = "heardle"
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("heardle/", views.heardle, name="heardle"),
]
