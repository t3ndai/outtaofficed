from django.urls import path
from . import views

urlpatterns = [
    path("items/<uuid:item_id>/", views.item_subscribe, name="item-subscribe")
]

