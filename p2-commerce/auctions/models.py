from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=64)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    start = models.FloatField()
    price = models.FloatField(default=0)
    status = models.BooleanField(default=1)
    image = models.URLField(default=None)
    owner = models.CharField(max_length=64, default='None')   # owner
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")

class Watchlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Bid(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.FloatField()
    numberOfBids = models.IntegerField(default=0)

class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.TextField()