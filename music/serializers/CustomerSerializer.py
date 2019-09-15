from rest_framework import serializers

from music.models import Customer
from music.serializers.UserSerialzier import UserSerializer


class CustomerSerialzier(serializers.ModelSerializer):
    user = UserSerializer
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'user')
