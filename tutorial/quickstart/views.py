from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from tutorial.quickstart.models import Tweet, UserFollow
from rest_framework import viewsets, mixins
from tutorial.quickstart.permissions import IsAuthorOrReadOnly
from tutorial.quickstart.serializers import (UserSerializer,
                                             TweetSerializer,
                                             UserFollowsSerializer,
                                             FollowersSerializer,
                                             FollowsSerializer)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-username')
    serializer_class = UserSerializer
    lookup_field = 'username'


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserTweetsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tweet.objects
    serializer_class = TweetSerializer

    def get_queryset(self):
        return self.queryset.filter(
            author__username=self.kwargs['parent_lookup_username']
        )


class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tweet.objects
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tweet.objects.filter(
            author__followers__follower=self.request.user
        )


class UserFollowsViewSet(viewsets.ModelViewSet):
    queryset = UserFollow.objects
    serializer_class = UserFollowsSerializer

    def perform_create(self, serializer):
        serializer.save(
            follower=self.request.user,
            follows=User.objects.get(username=self.kwargs[self.lookup_field])
        )

    def get_object(self):
        return self.queryset.filter(
            follower=self.request.user,
            follows__username=self.kwargs[self.lookup_field]
        )


class UserFollowsListViewSet(
    GenericViewSet,
    mixins.ListModelMixin
):
    queryset = UserFollow.objects
    serializer_class = FollowsSerializer

    def get_queryset(self):
        username = self.kwargs['parent_lookup_username']
        return self.queryset.filter(follower__username=username)


class UserFollowedListViewSet(
    GenericViewSet,
    mixins.ListModelMixin
):
    queryset = UserFollow.objects
    serializer_class = FollowersSerializer

    def get_queryset(self):
        username = self.kwargs['parent_lookup_username']
        return self.queryset.filter(follows__username=username)
