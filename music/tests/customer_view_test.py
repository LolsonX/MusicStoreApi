import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from jwt import decode

from MusicApi.settings import SIMPLE_JWT
from music.models.customer import Customer
from music.tests import BaseViewTest


class CustomerViewTest(BaseViewTest):
    def test_staff_should_get_list_of_customers(self):
        response = self.client.get(
            reverse("customers-all"),
            HTTP_AUTHORIZATION='Bearer {}'.format(self.login("staff", "1234qwer").data["access"])
        )
        # fetch the data from db
        expected = Customer.objects.all()
        serialized = CustomerSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_should_not_get_list_of_customers(self):
        response = self.client.get(
            reverse("customers-all"),
            HTTP_AUTHORIZATION='Bearer {}'.format(self.login("test", "1234qwer").data["access"])
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Only positive test because it is going to be token based
    def test_user_should_get_info_about_himself(self):
        response = self.client.get(
            reverse("customer"),
            HTTP_AUTHORIZATION='Bearer {}'.format(self.login("test", "1234qwer").data["access"])
        )
        decoded = (decode(response.data["access"], SIMPLE_JWT['SIGNING_KEY'], SIMPLE_JWT['ALGORITHM']))
        expected = Customer.objects.get(user_id=decoded["user_id"])
        serialized = CustomerSeriazlier(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_should_be_able_to_change_his_data_and_pass(self):
        response = self.client.put(
            reverse("customer"),
            data={},
            HTTP_AUTHORIZATION='Bearer {}'.format(self.login("test", "1234qwer").data["access"])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_should_not_be_able_to_change_username(self):
        response = self.client.put(
            reverse("customer"),
            HTTP_AUTHORIZATION='Bearer {}'.format(self.login("test", "1234qwer").data["access"])
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_should_be_able_to_change_email(self):
        response = self.client.put(
            reverse("customer"),
            HTTP_AUTHORIZATION='Bearer {}'.format(self.login("test", "1234qwer").data["access"])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_should_be_able_to_deactivate_account(self):
        response = self.client.delete(reverse("customer"),
                                      HTTP_AUTHORIZATION='Bearer {}'
                                      .format(self.login("test", "1234qwer")
                                              .data["access"]))
        decoded = (decode(response.data["access"], SIMPLE_JWT['SIGNING_KEY'], SIMPLE_JWT['ALGORITHM']))
        user = User.objects.get(pk=decoded["user_id"])
        self.assertFalse(user.is_active)

    def test_should_create_customer(self):
        for customer in self.valid_customers:
            count_before = Customer.objects.count()
            response = self.client.post(reverse("artists-all"),
                                        data=json.dumps(customer),
                                        content_type='application/json'
                                        )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(count_before + 1, Customer.objects.count())

    def test_should_not_create_customer(self):
        for customer in self.invalid_customers:
            count_before = Customer.objects.count()
            response = self.client.post(reverse("artists-all"),
                                        data=json.dumps(customer),
                                        content_type='application/json'
                                        )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(count_before, Customer.objects.count())