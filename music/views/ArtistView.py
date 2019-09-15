from rest_framework import generics
from music.models import Artist
from music.permissions.isStaffOrReadOnly import IsStaffOrReadOnly
from music.serializers import ArtistSerializer


class ListArtistView(generics.ListCreateAPIView):
    permission_classes = (IsStaffOrReadOnly,)
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class RetrieveUpdateDestroyArtistView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsStaffOrReadOnly, )
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()
    lookup_field = 'id'

    '''Custom retrieving if i would like to find those elements in some other way'''
    # def retrieve(self, request, *args, **kwargs):
    #     try:
    #         response = self.queryset.get(id=kwargs['id'], first_name=kwargs['first_name'])
    #     except ObjectDoesNotExist:
    #         raise Http404
    #     serialized = self.get_serializer(response)
    #     print(serialized)
    #     return Response(serialized.data)
