from django import forms

from .models import Tweet


class CreateTweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ("content",)

    content = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "いまどうしてる？"}),
    )
