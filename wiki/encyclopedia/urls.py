from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="index"),
    path("<str:title>", views.entry, name="entry"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("new/", views.new, name="new"),
    path("edit/", views.edit, name="edit"),
    path("random/", views.random, name="random"),
]
