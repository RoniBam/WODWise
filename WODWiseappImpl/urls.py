from django.urls import path

from . import views

app_name = 'WODWiseappImpl'

urlpatterns = [
    path("", views.index, name="index"),
    path("box/<int:box_id>/", views.box_detail, name="box_detail"),
    path("box/list/", views.box_list, name="box_list"),
    path("box/new/", views.box_create_form, name="box_create_form"),
    path("box/create/", views.box_create, name="box_create"),
    path("box/<int:box_id>/review/", views.add_review, name="add_review"),
]