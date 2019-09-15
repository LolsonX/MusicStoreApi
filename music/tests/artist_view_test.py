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
                                    HTTP_AUTHORIZATION='Bearer {}'.format(self.login("staff", "1234qwer").data["access"])
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(count_before + 1, Artist.objects.count())

        count_before = Artist.objects.count()
        response = self.client.post(reverse("artists-all"),
                                    data=json.dumps(self.valid_artist),
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION='Bearer {}'.format(self.login("admin", "1234qwer").data["access"])
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(count_before + 1, Artist.objects.count())

    def test_not_staff_should_not_create_artist(self):
        count_before = Artist.objects.count()
        response = self.client.post(reverse("artists-all"),
                                    data=json.dumps(self.invalid_artist),
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION='Bearer {}'.format(self.login("test", "1234qwer").data["access"])
                                    )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(count_before, Artist.objects.count())

    def test_unauthenticated_should_not_create_artist(self):
        count_before = Artist.objects.count()
        # Test with not logged user but not staff with correct data

        response = self.client.post(reverse("artists-all"),
                                    data=json.dumps(self.valid_artist),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(count_before, Artist.objects.count())

    def test_should_not_create_artist(self):
        count_before = Artist.objects.count()

        response = self.client.post(reverse("artists-all"),
                                    data=json.dumps(self.invalid_artist),
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION='Bearer {}'.format(
                                        self.login("staff", "1234qwer").data["access"])
                                    )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(count_before, Artist.objects.count())

        response = self.client.post(reverse("artists-all"),
                                    data=json.dumps(self.invalid_artist),
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION='Bearer {}'.format(
                                        self.login("admin", "1234qwer").data["access"])
                                    )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(count_before, Artist.objects.count())

    def test_should_update_artist(self):
        artist = self.create_artist("Karol", "Ostrowski")
        response = self.client.put(reverse("artists-detail", kwargs={'id': str(artist.id)}),
                                   data={"first_name": "Stefan", "last_name": "Burak"},
                                   HTTP_AUTHORIZATION='Bearer {}'.format(
                                       self.login("admin", "1234qwer").data["access"])
                                   )
        artist.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(artist.first_name, "Stefan")
        self.assertEqual(artist.last_name, "Burak")
        response = self.client.put(reverse("artists-detail", kwargs={'id': str(artist.id)}),
                                   data={"first_name": "Karol", "last_name": "Ostrowski"},
                                   HTTP_AUTHORIZATION='Bearer {}'.format(
                                       self.login("staff", "1234qwer").data["access"])
                                   )
        artist.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(artist.first_name, "Karol")
        self.assertEqual(artist.last_name, "Ostrowski")

    def test_unauthorized_should_not_update_artist(self):
        artist = self.create_artist("Karol", "Ostrowski")
        response = self.client.put(reverse("artists-detail", kwargs={'id': str(artist.id)}),
                                   data={"first_name": "", "last_name": ""}
                                   )
        artist.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(artist.first_name, "Karol")
        self.assertEqual(artist.last_name, "Ostrowski")

    def test_not_staff_should_not_update_artist(self):
        artist = self.create_artist("Karol", "Ostrowski")
        response = self.client.put(reverse("artists-detail", kwargs={'id': str(artist.id)}),
                                   data={"first_name": "Asd", "last_name": "Asd"},
                                   HTTP_AUTHORIZATION='Bearer {}'.format(
                                       self.login("test", "1234qwer").data["access"])
                                   )
        artist.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(artist.first_name, "Karol")
        self.assertEqual(artist.last_name, "Ostrowski")

    def test_should_not_update_artist(self):
        artist = self.create_artist("Karol", "Ostrowski")
        response = self.client.put(reverse("artists-detail", kwargs={'id': str(artist.id)}),
                                   data={"first_name": "", "last_name": ""},
                                   HTTP_AUTHORIZATION='Bearer {}'.format(
                                       self.login("admin", "1234qwer").data["access"])
                                   )
        artist.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(artist.first_name, "Karol")
        self.assertEqual(artist.last_name, "Ostrowski")

        response = self.client.put(reverse("artists-detail", kwargs={'id': str(artist.id)}),
                                   data={"first_name": "", "last_name": ""},
                                   HTTP_AUTHORIZATION='Bearer {}'.format(
                                       self.login("staff", "1234qwer").data["access"])
                                   )
        artist.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(artist.first_name, "Karol")
        self.assertEqual(artist.last_name, "Ostrowski")

    def should_delete_artist(self):
        pass

    def should_not_delete_artist(self):
        pass
