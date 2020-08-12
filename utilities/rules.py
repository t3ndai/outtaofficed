from django.contrib.auth.decorators import user_passes_test
from connections.models import Profile
from functools import wraps
from django.core.exceptions import PermissionDenied


def mailbox_member_exists(member, mailbox):
    return member.mailbox_member.filter(mailbox=mailbox).exists()


def mailbox_owner(member, mailbox):
    return member.mailboxes.filter(id=mailbox).exists()


def is_mailbox_member(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        member = Profile.objects.get(user_id=request.user.id)
        mailbox = kwargs["mailbox_id"]
        if not member:
            return False
        if mailbox_member_exists(member, mailbox) or mailbox_owner(member, mailbox):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap

