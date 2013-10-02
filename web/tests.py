from django.contrib.auth.models import User
from django.test import TestCase, Client
from viscommunityweb.settings import URL_PREPENDER


class URLTests(TestCase):
    client = Client()


    def setUp(self):
        self.adminuser = User.objects.create_user('test', 'admin@test.com', 'secret')
        self.adminuser.save()
        self.adminuser.is_staff = True
        self.adminuser.save()


    def testHome(self):
        response = self.client.get(URL_PREPENDER + '/')

        #test we actually have an ok response
        self.assertEqual(response.status_code, 200)


    def testLogin(self):
        response = self.client.get(URL_PREPENDER + '/accounts/login')

        self.client.login(username='test', password='secret')

        #test we actually have an ok response
        self.assertEqual(response.status_code, 200)


    def testProfile(self):
        self.client.login(username='test', password='secret')

        response = self.client.get(URL_PREPENDER + '/accounts/profile')

        #test we actually have an ok response
        self.assertEqual(response.status_code, 200)


    def testVolunteer(self):
        self.client.login(username='test', password='secret')

        response = self.client.get(URL_PREPENDER + '/volunteer')

        #test we actually have an ok response
        self.assertEqual(response.status_code, 200)


    def testContact(self):
        self.client.login(username='test', password='secret')

        response = self.client.get(URL_PREPENDER + '/contact')

        #test we actually have an ok response
        self.assertEqual(response.status_code, 200)


    def testLogout(self):
        self.client.login(username='test', password='secret')

        response = self.client.get(URL_PREPENDER + '/accounts/logout')

        #test we actually have an ok response
        self.assertEqual(response.status_code, 200)


