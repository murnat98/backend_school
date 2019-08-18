from django.test import TestCase
from django.urls import reverse


class ImportsTest(TestCase):
    def test_citizen_id(self):
        response = self.client.post(reverse('citizens:imports'), {'citizens': ''}, content_type='application/json')
