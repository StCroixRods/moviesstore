from django.db import models
from django.contrib.auth.models import User

class Petition(models.Model):
    movie_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    votes = models.ManyToManyField(User, related_name='voted_petitions', blank=True)

    def __str__(self):
        return self.movie_name

    def total_votes(self):
        return self.votes.count()