from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# user:Name (Harry, Hermione, Ron, Geenie)
# password: Name1234

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Listing(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=1024, blank=True)
    img_url = models.CharField(max_length=1024, blank=True)
    starting_bid = models.FloatField()
    max_bid = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings", blank=True, null=True)
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    watchers = models.ManyToManyField(User, related_name="watchlist", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed = models.BooleanField(default=False)
    last_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wins", blank=True, null=True)

    def __str__(self):
        return self.title


class Bid(models.Model):
    bid = models.FloatField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.bid)


class Comment(models.Model):
    comment = models.CharField(max_length=1024)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment
