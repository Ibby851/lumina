from django import forms
from .models import IndividualChat


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model=IndividualChat
        fields=['content']


class FileMessageForm(forms.ModelForm):
    class Meta:
        model = IndividualChat
        fields = ['file']

