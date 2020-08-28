from django.urls import path, include
from .views import (
    CreateCollectionView,
    CreateItemView,
    collection_detail,
    item_detail,
    user_collection_list,
    user_item_list,
    create_comment,
    get_comments,
)

urlpatterns = [
    path("", user_item_list, name="items"),
    path("create/", CreateItemView.as_view(), name="create-item"),
    path("create/mardownx/", include("markdownx.urls")),
    path("<uuid:item_id>/", item_detail, name="item-detail"),
    path("<uuid:item_id>/reply", create_comment, name="create-comment"),
    path("<uuid:item_id>/comments", get_comments, name="get-comments"),
    path(
        "collections/create", CreateCollectionView.as_view(), name="create-collection"
    ),
    path("collections/", user_collection_list, name="collections"),
    path(
        "collections/<uuid:collection_id>/", collection_detail, name="collection-detail"
    ),
]
