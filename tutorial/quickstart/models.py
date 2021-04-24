from django.db import models
from django.contrib.auth.models import User


class Tweet(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.CharField(max_length=600)
    photo = models.URLField(max_length=300, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'[{self.author.username}] {self.text}'


class UserFollow(models.Model):
    follower = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='follows')
    follows = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='followers')
    followed = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-followed']

    def __str__(self):
        return f'{self.follower.username} -> {self.follows.username}'


