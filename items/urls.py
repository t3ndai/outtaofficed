from django.urls import path
from .views import (
    CreateCollectionView,
    CreateItemView,
    collection_detail,
    item_detail,
    user_collection_list,
    user_item_list,
)

urlpatterns = [
    path("", user_item_list, name="items"),
    path("create/", CreateItemView.as_view(), name="create-item"),
    path("<uuid:item_id>/", item_detail, name="item-detail"),
    path(
        "collections/create", CreateCollectionView.as_view(), name="create-collection"
    ),
    path("collections/", user_collection_list, name="collections"),
    path(
        "collections/<uuid:collection_id>/", collection_detail, name="collection-detail"
    ),
]
