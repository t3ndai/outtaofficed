from django.urls import path
from . import views

urlpatterns = [
    path("profile/create", views.CreateProfileView.as_view(), name="create-profile"),
    path("profile/<uuid:pk>", views.ProfileDetailView.as_view(), name="profile-detail"),
    path(
        "profile/<uuid:pk>/update",
        views.UpdateProfileView.as_view(),
        name="profile-update",
    ),
]
