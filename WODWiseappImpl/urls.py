from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("box/<int:box_id>/", views.box_detail, name="box_detail"),
    path("box/list/", views.box_list, name="box_list"),
    path("box/new/", views.box_create_form, name="box_create_form"),
    path("box/create/", views.box_create, name="box_create"),
]