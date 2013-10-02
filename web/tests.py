from django.test import TestCase, Client
from viscommunityweb.settings import URL_PREPENDER


class URLTests(TestCase):
    client = Client()

    def testHome(self):
        response = self.client.get(URL_PREPENDER + '/')

        #test we actually have an ok response
        self.assertEqual(response.status_code, 200)

    def testLogin(self):
        response = self.client.get(URL_PREPENDER + '/')

        #test we actually have an ok response
        self.assertEqual(response.status_code, 200)

    def testHome(self):
        response = self.client.get(URL_PREPENDER + '/')

        #test we actually have an ok response
        self.assertEqual(response.status_code, 200)


