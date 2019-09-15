import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from music.models import Song, Artist


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_artist(first_name, last_name=None):
        return Artist.objects.create(first_name=first_name, last_name=last_name)

    @staticmethod
    def create_song(title, artist):
        return Song.objects.create(title=title, artist=artist)

    @staticmethod
    def create_user(username, password):
        u = User.objects.create()
        u.username = username
        u.set_password(password)
        u.save()
        return u

    def setUp(self):
        # add test data
        users = [
            {"username": "test", "password": "1234qwer"}
        ]
        db_users = [self.create_user(user["username"], user["password"]) for user in users]
        artists = [
            self.create_artist("Sean", "Paul"),
            self.create_artist("Konshens"),
            self.create_artist("Brick and Lace"),
            self.create_artist("Damien", "Marley")]
        songs = [
            self.create_song("like glue", artists[0]),
            self.create_song("simple song", artists[1]),
            self.create_song("love is wicked", artists[2]),
            self.create_song("jam rock", artists[3])
        ]
        self.valid_artist = {'first_name': "Karol", 'last_name': "Ostrowski"}
        self.invalid_artist = {'first_name': '', 'last_name': ''}

    def login(self, username, password):
        return self.client.post(reverse("token_obtain_pair"), {"username": username, "password": password})

