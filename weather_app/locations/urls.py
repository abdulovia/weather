from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "locations"
urlpatterns = [
    path("search/", views.search, name="search"),
    path("faq/", TemplateView.as_view(template_name="faq.html"), name="faq"),
    path(
        "features/",
        TemplateView.as_view(template_name="features.html"),
        name="features",
    ),
    path("add/", views.add, name="add"),
    path("delete/", views.delete, name="delete"),
    path("", views.home, name="home"),
]
