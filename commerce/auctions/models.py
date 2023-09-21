from django.contrib.auth.models import AbstractUser
from django.utils import *
from django.db import models

class User(AbstractUser):
    pass

class entries(models.Model):
    user = models.CharField(max_length=255)
    highestbiduser = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    image = models.ImageField()
    detail = models.TextField()
    bid = models.IntegerField()
    category = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"user is {self.user}, highest bidder is {self.highestbiduser}, title is {self.title}, image is {self.image}, details are {self.detail}, bid amount is {self.bid}, Category is {self.category}, time is {self.timestamp}"

class comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_users")
    title = models.ForeignKey(entries, on_delete=models.CASCADE, related_name="comments_entry")
    comment = models.TextField()

    def __str__(self):
        return f"user is {self.user}, title is {self.title}, comment is {self.comment}"

class new_bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_users")
    entry = models.ForeignKey(entries, on_delete=models.CASCADE, related_name="bid_entry")
    bid = models.IntegerField()

    def __str__(self):
        return f"user is {self.user}, entry is {self.entry}, bid is {self.bid}"

class closed_entries(models.Model):
    user = models.CharField(max_length=255)
    highestbiduser = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    image = models.ImageField()
    detail = models.TextField()
    bid = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"user is {self.user}, highest bidder is {self.highestbiduser}, title is {self.title}, image is {self.image}, details are {self.detail}, bid amount is {self.bid}, time is {self.timestamp}"

class user_watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")
    entry = models.ForeignKey(entries, on_delete=models.CASCADE, related_name="watchlist_entries")

    def __str__(self):
        return f" current user using watchlist is {self.user}, entry saved is {self.entry}"