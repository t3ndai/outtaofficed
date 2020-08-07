from django import forms
from .models import Mailbox


class MailboxForm(forms.Form):
    PRIVATE = "P"
    PRIVATE_LIMITED = "PL"
    MAILBOX_TYPES = [(PRIVATE, "Private"), (PRIVATE_LIMITED, "Private Limited")]
    name = forms.CharField(label="Name", max_length=75)
    member_email = forms.EmailField(
        label="Add member by email", required=False, max_length=200
    )
    member_alias = forms.CharField(
        label="Add member by alias", required=False, max_length=75
    )
    mailbox_type = forms.ChoiceField(label="Group Type", choices=MAILBOX_TYPES)


class TopicForm(forms.Form):
    members = forms.ModelMultipleChoiceField(
        queryset=None, widget=forms.CheckboxSelectMultiple()
    )
    name = forms.CharField(max_length=75)
    email_replies = forms.BooleanField()

    def __init__(self, member_query, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["members"].queryset = member_query
