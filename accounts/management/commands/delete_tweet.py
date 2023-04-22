from django.core.management.base import BaseCommand

from tweets.models import Tweet


class Command(BaseCommand):
    help = "Delete all tweets in bulk"

    def handle(self, *args, **kwargs):
        Tweet.objects.all().delete()
        print("finish delete")
