from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from .models import Profile

# Create your views here.
class CreateProfileView(CreateView):
    model = Profile
    fields = ["screen_name", "alias"]
    template_name = "create_profile.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateProfileView(UpdateView):
    model = Profile
    fields = ["screen_name", "alias"]


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "profile_detail.html"
