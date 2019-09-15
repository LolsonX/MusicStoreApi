import json

from django.urls import reverse
from rest_framework import status

from music.models import Artist
from music.serializers import ArtistSerializer
from music.tests import BaseViewTest


class ArtistViewTest(BaseViewTest):
    def test_get_all_artists(self):
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the songs/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("artists-all")
        )
        # fetch the data from db
        expected = Artist.objects.all()
        serialized = ArtistSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_get_artist(self):
        expected = Artist.objects.all().first()
        serialized = ArtistSerializer(expected, many=False)
        response = self.client.get(
            reverse("artists-detail", kwargs={'id': str(expected.id)})
        )
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_not_get_artist(self):
        response = self.client.get(
            reverse("artists-detail", kwargs={'id': str(999)}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_create_artist(self):
        count_before = Artist.objects.count()
        response = self.client.post(reverse("artists-all"),
                                    data=json.dumps(self.valid_artist),
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION='Bearer {}'.format(self.login("test", "1234qwer").data["access"])
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(count_before + 1, Artist.objects.count())

    def test_should_not_create_artist(self):
        count_before = Artist.objects.count()
        response = self.client.post(reverse("artists-all"),
                                    data=json.dumps(self.valid_artist),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(count_before, Artist.objects.count())
        response = self.client.post(reverse("artists-all"),
                                    data=json.dumps(self.invalid_artist),
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION='Bearer {}'.format(self.login("test", "1234qwer").data["access"])
                                    )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(count_before, Artist.objects.count())

    def test_should_update_artist(self):
        artist = self.create_artist("Karol", "Ostrowski")
        response = self.client.put(reverse("artist-update"),
                                   json.dumps({"first_name": "Stefan", "last_name": "Burak"}),
                                   kwargs={'id': str(artist.id)})
        artist.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(artist.first_name, "Stefan")
        self.assertEqual(artist.last_name, "Burak")

    def test_should_not_update_artist(self):
        artist = self.create_artist("Karol", "Ostrowski")
        response = self.client.put(reverse("artist-update"),
                                   json.dumps({"first_name": "", "last_name": ""}),
                                   kwargs={'id': str(artist.id)})
        artist.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(artist.first_name, "")
        self.assertNotEqual(artist.last_name, "")
