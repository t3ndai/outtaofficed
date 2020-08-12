from django.shortcuts import render, redirect
from .forms import MailboxForm, TopicForm
from django.views.generic.edit import FormView
from accounts.models import Profile
from .models import Mailbox, Topic
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from utilities import rules


class CreateMailboxView(FormView):
    template_name = "create_mailbox.html"
    form_class = MailboxForm

    def form_valid(self, form):
        owner = Profile.objects.get(user_id=self.request.user.pk)
        name = form.cleaned_data["name"]
        form_member_email = form.cleaned_data["member_email"]
        form_member_alias = form.cleaned_data["member_alias"]

        members = []
        if bool(form_member_email):
            member = Profile.objects.get(user__email=form_member_email)
            members.append(member)

        if bool(form_member_alias):
            member = Profile.objects.get(alias=form_member_alias)

        mailbox = owner.mailbox_owner.create(name=name)
        for member in members:
            mailbox.members.add(member)

        return redirect(reverse("home"))


@login_required
def mailbox_list(request):
    profile = Profile.objects.get(user_id=request.user.id)
    mailboxes = profile.mailboxes.all()

    return render(request, "mailbox_list.html", {"mailboxes": mailboxes})


@login_required
@rules.is_mailbox_member
def mailbox_detail(request, mailbox_id):
    mailbox = Mailbox.objects.get(id=mailbox_id)

    return render(request, "mailbox_detail.html", {"mailbox": mailbox})


@login_required
def create_topic_view(request, mailbox_id):

    members_query = Mailbox.objects.get(id=mailbox_id).members.all()
    if request.method == "POST":
        form = TopicForm(members_query, request.POST)

        if form.is_valid():
            members = form.cleaned_data["members"]
            name = form.cleaned_data["name"]
            email_replies = form.cleaned_data["email_replies"]
            mailbox = Mailbox.objects.get(id=mailbox_id)
            creator = Profile.objects.get(user_id=request.user.id)

            topic = Topic(
                name=name, mailbox=mailbox, email_replies=email_replies, creator=creator
            )
            topic.save()

            for member in members:
                topic.member.add(member)

            return redirect(reverse("home"))

    else:
        form = TopicForm(members_query)

    return render(request, "create_topic.html", {"form": form})

