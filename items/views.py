from connections.views import topic_detail
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView, CreateView
from django.views.generic import ListView
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed
from django.urls import reverse
from django.db.models import Prefetch, Q

from .forms import ItemForm, CommentForm
from .models import Item, ItemImage, Collection
from accounts.models import Profile
from connections.models import Topic
from events.updates import comment_update

import logging
import bleach
import json

logger = logging.getLogger(__name__)

# Create your views here.
class CreateItemView(FormView):
    template_name = "create_item.html"
    form_class = ItemForm
    success_url = "/items/"

    def form_valid(self, form):
        body_json = json.loads(form.cleaned_data["body"])
        tags = form.cleaned_data["tags"]
        owner = self.request.user
        body = body_json["html"]

        item = Item(body=body, tags=[tags], owner=owner)
        item.save()
        files = self.request.FILES.getlist("image")
        for file in files:
            image = ItemImage(image=file, item=item)
            image.save()

        return redirect(reverse("home"))


def user_item_list(request):
    owner = Profile.objects.get(user=request.user)
    items = Item.objects.filter(owner=owner)
    return render(request, "item_list.html", {"items": items})


def item_detail(request, item_id):
    item = Item.objects.filter(id=item_id).prefetch_related("comments").first()
    comments = list(item.comments.all())
    media = ItemImage.objects.filter(item=item_id)

    return render(
        request,
        "item_detail.html",
        {"item": item, "media": media, "comments": comments},
    )


def create_topic_item(request, topic_id):
    if request.method == "POST":
        form = ItemForm(request.POST)

        if form.is_valid():
            body_json = json.loads(form.cleaned_data["body"])
            tags = form.cleaned_data["tags"]
            owner = Profile.objects.get(user_id=request.user.pk)
            topic = Topic.objects.get(id=topic_id)
            body = body_json["html"]

            item = topic.topic_items.create(body=body, tags=[tags], owner=owner)
            files = request.FILES.getlist("image")
            for file in files:
                item_file = ItemImage(image=file, item=item)
                item_file.save()

            return redirect(reverse("home"))
    else:
        form = ItemForm()

    return render(request, "create_item.html", {"form": form})


def create_comment(request, item_id):
    if request.method == "POST":
        form = ItemForm(request.POST)

        if form.is_valid():
            body_json = json.loads(form.cleaned_data["body"])
            tags = form.cleaned_data["tags"]

            body = body_json["html"]

            owner = Profile.objects.get(user_id=request.user.pk)
            item = Item.objects.get(id=item_id)

            comment = item.comments.create(body=body, owner=owner, tags=[tags])

            comment_update(item_id)

            files = request.FILES.getlist("image")
            for file in files:
                item_file = ItemImage(image=file, item=comment)
                item_file.save()

            return redirect("item-detail", item_id=item_id)
    else:
        form = ItemForm()

    return render(request, "create_comment.html", {"form": form, "item_id": item_id})


def get_comments(request, item_id):
    comments = Item.objects.filter(parent=item_id)
    return render(request, "comments.html", {"comments": comments})


## Collections


class CreateCollectionView(CreateView):
    model = Collection
    template_name = "create_collection.html"
    fields = ["name", "tags"]
    success_url = "/items/collections"

    def form_valid(self, form):
        owner = Profile.objects.get(user_id=self.request.user.pk)
        name = form.cleaned_data["name"]
        tags = form.cleaned_data["tags"]

        owner.owner_collections.create(name=name, tags=tags)
        return super().form_valid(form)


def user_collection_list(request):
    owner = Profile.objects.get(user_id=request.user.pk)
    collections = Collection.objects.filter(owners=owner)
    return render(request, "collection_list.html", {"collections": collections})


def collection_detail(request, collection_id):
    collection = Collection.objects.get(id=collection_id)
    return render(request, "collection_detail.html", {"collection": collection})
