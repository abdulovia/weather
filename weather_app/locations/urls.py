from django.urls import path
from . import views

app_name = "locations"
urlpatterns = [
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add"),
    path("delete/", views.delete, name="delete"),
    path("", views.home, name="home"),
]
