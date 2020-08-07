from django.urls import path
from . import views

urlpatterns = [
    path("mailbox/create", views.CreateMailboxView.as_view(), name="create-mailbox"),
    path("mailbox/list", views.mailbox_list, name="mailbox-list"),
    path("mailbox/<uuid:mailbox_id>", views.mailbox_detail, name="mailbox-detail"),
    path(
        "mailbox/<uuid:mailbox_id>/topics/create",
        views.create_topic_view,
        name="create-topic",
    ),
]
