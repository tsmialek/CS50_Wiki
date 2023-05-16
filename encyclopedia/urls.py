from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("add_page", views.add_page, name="add_page"),
    path("random_page", views.random_page, name="random_page"),
    path('edit_page/<str:entry>', views.edit_page, name="edit_page")
]
