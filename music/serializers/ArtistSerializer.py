from rest_framework import serializers

from music.models import Artist


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ("first_name", "last_name")
