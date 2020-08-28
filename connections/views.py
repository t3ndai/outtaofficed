from django.shortcuts import render, redirect
from django.db.models import Prefetch, Q
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView

from .forms import MailboxForm, TopicForm

from accounts.models import Profile

from .models import Mailbox, Topic
from items.models import Item

from utilities import rules

import logging


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

        mailbox = owner.mailboxes_owned.create(name=name)
        for member in members:
            mailbox.members.add(member)

        return redirect(reverse("home"))


@login_required
def mailbox_list(request):
    profile = (
        Profile.objects.filter(user_id=request.user.id)
        .prefetch_related(
            Prefetch("mailboxes", to_attr="mailboxes_in"),
            Prefetch("mailboxes_owned", to_attr="my_mailboxes"),
        )
        .first()
    )
    mailboxes_ = Mailbox.objects.filter(
        Q(owner=request.user.id) | Q(members=request.user.id)
    )
    return render(request, "mailbox_list.html", {"mailboxes": mailboxes_})


@login_required
@rules.is_mailbox_member
def mailbox_detail(request, mailbox_id):
    user_topics = Topic.objects.filter(member=request.user.id)
    mailbox = (
        Mailbox.objects.filter(id=mailbox_id)
        .prefetch_related(
            Prefetch("mailbox_topics", queryset=user_topics, to_attr="topics")
        )
        .first()
    )

    topics = list(mailbox.topics)

    return render(
        request, "mailbox_detail.html", {"mailbox": mailbox, "topics": topics}
    )


@login_required
@rules.is_mailbox_member
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

            topic = creator.topics.create(
                name=name,
                mailbox=mailbox,
                email_replies=email_replies,
                through_defaults={"creator": creator},
            )

            for member in members:
                topic.member.add(member)

            return redirect(reverse("home"))

    else:
        form = TopicForm(members_query)

    return render(request, "create_topic.html", {"form": form})


@login_required
# @rules.is_mailbox_member
def topic_detail(request, topic_id):
    posts_query = Item.objects.filter(topic=topic_id)
    topic = (
        Topic.objects.filter(id=topic_id)
        .prefetch_related(
            Prefetch("topic_items", queryset=posts_query, to_attr="posts")
        )
        .first()
    )

    posts = list(topic.posts)

    return render(request, "topic_detail.html", {"topic": topic, "posts": posts})
