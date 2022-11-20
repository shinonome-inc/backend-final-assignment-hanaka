from django import forms

from .models import Tweet


class CreateTweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ("content",)

        widget = forms.Textarea(
            attrs={
                "rows": 4,
                "cols": 35,
                "placeholder": "いまどうしてる？",
            }
        )