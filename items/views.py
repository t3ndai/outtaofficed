from items.models import Item
from django.shortcuts import render
from django.views.generic.edit import FormView, CreateView
from django.views.generic import ListView
from .forms import ItemForm
from .models import Item, ItemImage, Collection
from accounts.models import Profile
from django.http import HttpResponseRedirect
import logging

logger = logging.getLogger(__name__)

# Create your views here.
class CreateItemView(FormView):
    template_name = "create_item.html"
    form_class = ItemForm
    success_url = "/items/"

    def form_valid(self, form):
        body = form.cleaned_data["body"]
        tags = form.cleaned_data["tags"]
        owner = self.request.user

        item = Item(body=body, tags=[tags], owner=owner)
        item.save()
        files = self.request.FILES.getlist("image")
        for file in files:
            image = ItemImage(image=file, item=item)
            image.save()

        return HttpResponseRedirect("/")


def user_item_list(request):
    owner = request.user
    items = Item.objects.filter(owner=owner)
    return render(request, "item_list.html", {"items": items})


def item_detail(request, item_id):
    item = Item.objects.get(id=item_id)
    media = ItemImage.objects.filter(item=item_id)
    return render(request, "item_detail.html", {"item": item, "media": media})


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
