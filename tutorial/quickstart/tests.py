from django.test import TestCase
from tutorial.quickstart.models import *
from django.contrib.auth.models import User


class UsersTestCase(TestCase):
    def test_request_list_users_without_users(self):
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

    def test_request_list_users(self):
        User.objects.create(username='Leon')
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [{
                "url": "http://testserver/v1/users/Leon/",
                "username": "Leon",
                "email": "",
                "last_name": "",
                "first_name": ""}

            ]
            }
        )


class FollowTestCreate(TestCase):
    def setUp(self):
        self.User1 = User.objects.create(username='Leon')
        self.User2 = User.objects.create(username='Rosa')
        self.User3 = User.objects.create(username='Kolt')
        UserFollow.objects.create(follower=self.User1, follows=self.User2)

    def test_data_exist(self):
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(UserFollow.objects.count(), 1)

    def test_new_follow_connect(self):
        self.client.force_login(self.User1)
        response = self.client.post(f'/v1/follow/{self.User2.username}/')
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(UserFollow.objects.filter(
            follower=self.User1,
            follows=self.User2
        ))

    def test_new_unfollow_connect(self):
        self.client.force_login(self.User1)
        response = self.client.delete(f'/v1/follow/{self.User2.username}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(UserFollow.objects.count(), 0)


