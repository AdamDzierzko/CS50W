from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    numberOfFollowers = models.IntegerField(default=0)
    numberOfFollowing = models.IntegerField(default=0)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    numberOfLikes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "text": self.text,
#            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "timestamp": self.timestamp.strftime(" %m-%d-%Y %H:%M %p"),
            "numberOfLikes": self.numberOfLikes
        }


class Follow(models.Model):
    follower_id  = models.ForeignKey(User, on_delete=models.CASCADE)
    following_id = models.IntegerField()

class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)