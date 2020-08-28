"""outtaofficed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache

from ckeditor_uploader import views as uploader_views

from connections import views as connection_views
from items import views as item_views

topics_urls = [
    path("<uuid:topic_id>", connection_views.topic_detail, name="topic-detail"),
    path(
        "<uuid:topic_id>/item/create",
        item_views.create_topic_item,
        name="create-topic-item",
    ),
]

urlpatterns = [
    path("", include("pages.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("accounts.urls")),
    path("items/", include("items.urls")),
    path("connections/", include("connections.urls")),
    path("markdownx/", include("markdownx.urls")),
    path("ckeditor/upload/", uploader_views.upload, name="ckeditor_upload"),
    path(
        "ckeditor/browse/", never_cache(uploader_views.browse), name="ckeditor_browse"
    ),
    path("topics/", include(topics_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
