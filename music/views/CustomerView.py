from rest_framework import generics

from music.models.customer import Customer
from music.serializers.CustomerSerializer import CustomerSerializer

class ListCustomerView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer