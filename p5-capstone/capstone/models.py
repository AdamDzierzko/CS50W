from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass

class Genere(models.Model):
    genere_name = models.TextField(blank=True)

class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    title = models.TextField(blank=True)
    genere = models.ForeignKey(Genere, on_delete=models.CASCADE, related_name="genere", default=None)
    director = models.TextField(blank=True)
    description = models.TextField(blank=True)
    year = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    numberOfComents = models.IntegerField(default=0)
    numberOfGrades = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "title": self.title,
            "genere": self.genere.genere_name,
            "director": self.director,
            "description": self.description,
            "year": self.year,
            "timestamp": self.timestamp.strftime(" %m-%d-%Y %H:%M %p"),
            "numberOfComents": self.numberOfComents,
            "numberOfGrades": self.numberOfGrades
        }


class Coment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    textComent = models.TextField(blank=True)

class Grade(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    grade = models.FloatField(default=0)

class Actor(models.Model):
    actor_name =  models.TextField(blank=True)

class ActorMovie(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor_id = models.ForeignKey(Actor, on_delete=models.CASCADE)


