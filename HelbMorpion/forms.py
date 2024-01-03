from django import forms
from .models import CommunityMessage


class CommunityMessageForm(forms.ModelForm):
    class Meta:
        model = CommunityMessage
        fields = ['email', 'subject', 'message']

    # You can customize the form further if needed, for example, adding widgets or validators.
