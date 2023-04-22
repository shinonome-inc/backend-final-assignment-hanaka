import random

from django.core.management.base import BaseCommand

from tweets.models import Tweet

from ...models import User


class Command(BaseCommand):
    help = "Create 5000 tweets in bulk"

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        tweets = []
        for i in range(5000):
            contents = f"Tweet {i}"
            user = random.choice(users)
            tweets.append(Tweet(contents=contents, user=user))
        Tweet.objects.bulk_create(tweets)
        print("created 5000 tweets")
