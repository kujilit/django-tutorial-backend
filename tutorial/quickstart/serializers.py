from django.contrib.auth.models import User
from rest_framework import serializers
from tutorial.quickstart.models import Tweet
from tutorial.quickstart.models import UserFollow


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'last_name', 'first_name']
        extra_kwargs = {'url': {'lookup_field': 'username'}}


class TweetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['url', 'id', 'text', 'author', 'created', 'photo']


class UserFollowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = []


class FollowsSerializer(serializers.ModelSerializer):
    follows = UserSerializer(read_only=True)

    class Meta:
        model = UserFollow
        fields = ['follows', 'followed']


class FollowersSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)

    class Meta:
        model = UserFollow
        fields = ['follower', 'followed']
