from django.urls import reverse
from rest_framework.views import status
from music.models import Song
from music.serializers import SongSerializer
from music.tests.base_view_test import BaseViewTest


class SongViewTest(BaseViewTest):
    def test_get_all_songs(self):
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the songs/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("songs-all")
        )
        # fetch the data from db
        expected = Song.objects.all()
        serialized = SongSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
