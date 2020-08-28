from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core import validators
from django.urls import reverse

# Create your models here.
class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        "accounts.Profile", on_delete=models.CASCADE, related_name="items"
    )
    body = models.TextField(validators.MinLengthValidator(2))
    created_at = models.DateTimeField(auto_now=True)
    tags = ArrayField(models.CharField(max_length=200), blank=True)
    topic = models.ForeignKey(
        "connections.Topic",
        on_delete=models.CASCADE,
        null=True,
        related_name="topic_items",
    )
    parent = models.ForeignKey(
        "self", null=True, on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self):
        return self.body[:50]

    def get_absolute_url(self):
        return reverse("item", kwargs={"pk": self.pk})


class ItemImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now=True)


class Collection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    items = models.ManyToManyField(Item, related_name="items_collections")
    name = models.CharField(default="saved items", max_length=75)
    collections = models.ManyToManyField("self", related_name="collections_collections")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    owners = models.ManyToManyField(
        "accounts.Profile", related_name="owner_collections"
    )
    tags = ArrayField(models.CharField(max_length=200), blank=True)

