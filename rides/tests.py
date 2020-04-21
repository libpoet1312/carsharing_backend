from django.test import TestCase
from rest_framework.test import APITestCase


# Create your tests here.
class HttpTripTest(APITestCase):
    pass
    # def test_user_can_list_trips(self):
    #     trips = [
    #         Trip.objects.create(pick_up_address='A', drop_off_address='B'),
    #         Trip.objects.create(pick_up_address='B', drop_off_address='C')
    #     ]
    #     response = self.client.get(reverse('trip:trip_list'),
    #         HTTP_AUTHORIZATION=f'Bearer {self.access}'
    #     )
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     exp_trip_ids = [str(trip.id) for trip in trips]
    #     act_trip_ids = [trip.get('id') for trip in response.data]
    #     self.assertCountEqual(exp_trip_ids, act_trip_ids)