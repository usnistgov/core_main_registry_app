"""Forms for admin views
"""
from django import forms


class UploadCustomResourcesForm(forms.Form):
    """
    Form to upload new Custom Resources
    """

    json_file = forms.FileField(
        label="Select a file",
        required=True,
        widget=forms.FileInput(attrs={"accept": ".json"}),
    )
