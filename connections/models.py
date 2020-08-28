from django.db import models
import uuid
from accounts.models import Profile
from outtaofficed.settings import DOMAIN
from secrets import token_urlsafe


def generate_address():
    return f"{token_urlsafe(8)+'@'+DOMAIN}"


# Create your models here.
class Mailbox(models.Model):
    PRIVATE = "P"
    PRIVATE_LIMITED = "PL"
    MAILBOX_TYPES = [(PRIVATE, "Private"), (PRIVATE_LIMITED, "Private Limited")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        "accounts.Profile", on_delete=models.CASCADE, related_name="mailboxes_owned"
    )
    name = models.CharField(max_length=75)
    members = models.ManyToManyField(
        "accounts.Profile", through="MailboxDetail", related_name="mailboxes",
    )
    address = models.EmailField(unique=True, default=generate_address())
    mailbox_type = models.CharField(
        max_length=2, choices=MAILBOX_TYPES, default=PRIVATE
    )

    def __str__(self):
        return self.name


class MailboxDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mailbox = models.ForeignKey(
        Mailbox, on_delete=models.CASCADE, related_name="mailbox"
    )
    member = models.ForeignKey(
        "accounts.Profile", on_delete=models.CASCADE, related_name="mailbox_member"
    )
    date_added = models.DateField(auto_now=True)


def create_dict(member):
    return dict(id=member.user_id, name=member.screen_name, alias=member.alias)


def members_in_group_dict(mailbox_id):
    """
        1. query members in members 
        2. construct dictionary with members 
        3. return dict 
    """
    mailbox = Mailbox.objects.get(id=mailbox_id)
    members = mailbox.members.all()
    return {"members": list(map(create_dict, members))}


class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mailbox = models.ForeignKey(
        Mailbox, on_delete=models.CASCADE, related_name="mailbox_topics"
    )
    name = models.CharField(null=False, blank=False, max_length=75, editable=False)
    created_on = models.DateField(auto_now=True)
    member = models.ManyToManyField(
        "accounts.Profile",
        through="TopicDetail",
        through_fields=("topic", "member"),
        related_name="topics",
    )
    email_replies = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        return self.name


class TopicDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="topic")
    member = models.ForeignKey(
        "accounts.Profile", related_name="topic_member", on_delete=models.CASCADE
    )
    creator = models.ForeignKey(
        "accounts.Profile",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="topics_created",
    )
    notifications = models.BooleanField(default=True)
