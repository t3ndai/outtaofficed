from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, blank=False)

    REQUIRED_FIELDS = ["email"]


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, primary_key=True, on_delete=models.CASCADE)
    screen_name = models.CharField(unique=True, max_length=75)

    def __str__(self):
        return self.screen_name

    def get_absolute_url(self):
        reverse("profile-detail", kwargs={"pk": self.pk})

