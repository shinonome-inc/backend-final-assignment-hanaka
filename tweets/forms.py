from django import forms

from .models import Tweet


class CreateTweetForm(forms.ModelForm):
    content = forms.CharField(
        max_length=140,
        widget=forms.Textarea(attrs={"rows": 4, "cols": 35, "placeholder": "いまどうしてる？"}),
    )

    class Meta:
        model = Tweet
        fields = ("content",)
