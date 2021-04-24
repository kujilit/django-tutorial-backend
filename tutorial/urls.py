from django.contrib import admin
from django.urls import include, path
from rest_framework_extensions.routers import ExtendedDefaultRouter
from tutorial.quickstart import views
from tutorial.quickstart.router import SwitchDetailRouter

router = ExtendedDefaultRouter()
switch_router = SwitchDetailRouter()

user_route = router.register(r'users', views.UserViewSet)
user_route.register('tweets', views.UserTweetsViewSet, 'user-tweets', ['username'])
user_route.register('follows', views.UserFollowsListViewSet, 'follows', ['username'])
user_route.register('followed', views.UserFollowedListViewSet, 'follows', ['username'])

router.register(r'tweets', views.TweetViewSet)
router.register(r'feed', views.FeedViewSet)
switch_router.register(r'follow', views.UserFollowsViewSet)


urlpatterns = [
    path('v1/', include(switch_router.urls)),
    path('v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
