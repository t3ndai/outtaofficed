from django import forms
from .models import Item, ItemImage


class ItemForm(forms.Form):
    body = forms.CharField(label="Pintext", widget=forms.Textarea)
    image = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={"multiple": True, "data-max-files": 5, "data-max-file-size": "5MB"},
        ),
        label="Image Attachments",
        required=False,
    )
    tags = forms.CharField(max_length=200)


class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ("image",)


ImageItemFormSet = forms.inlineformset_factory(
    Item, ItemImage, form=ItemImageForm, fields=("image",)
)
