from django.test import TestCase, Client
from viscommunityweb.settings import URL_PREPENDER


class URLTests(TestCase):
    client = Client()

    def testHome(self):
        response = self.client.get(URL_PREPENDER + '/')
        print response

