from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from music.views import ListSongView
from music.views.ArtistView import ListArtistView, RetrieveUpdateDestroyArtistView

urlpatterns = [
    path('songs/', ListSongView.as_view(), name="songs-all"),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('artists/', ListArtistView.as_view(), name="artists-all"),
    path('artists/<int:id>', RetrieveUpdateDestroyArtistView.as_view(), name="artists-detail"),
    path('customers/', ListCustomerView.as_view(), name="customers-all"),
    path('customer', RetrieveUpdateDestroyCustomerView.as_view(), name="customer")
]
