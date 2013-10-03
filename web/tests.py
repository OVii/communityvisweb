from django.contrib.auth.models import User
from django.test import TestCase, Client
from taxonomy_init import taxonomy_init
from viscommunityweb.settings import URL_PREPENDER
from web.models import TaxonomyItem



class URLTests(TestCase):

    """
        To run these tests, run
        python manage.py test web
    """
    client = Client()


    def setUp(self):
        self.adminuser = User.objects.create_user('test', 'admin@test.com', 'secret')
        self.adminuser.save()
        self.adminuser.is_staff = True
        self.adminuser.save()

        taxonomy_init()


    def testHome(self):
        response = self.client.get(URL_PREPENDER + '/')

        #test we actually have an ok response
        self.assertEqual(response.status_code, 200)


    def testLogin(self):
        response = self.client.post(URL_PREPENDER + '/accounts/login/', {'username': 'test', 'password': 'secret'})
        self.assertRedirects(response, URL_PREPENDER + '/accounts/profile/', status_code=302, target_status_code=200)


    def testLoginAndCheckProfile(self):
        self.testLogin()

        response = self.client.get(URL_PREPENDER + '/accounts/profile/')

        #test we actually have an ok response
        self.assertEqual(response.status_code, 200)


    def testTaxonomyPageWithNoLogin(self):
        response = self.client.get(URL_PREPENDER + '/taxonomy/')

        #test we actually have an ok response
        self.assertEqual(response.status_code, 200)


    def testTaxonomyItemPageWithNoLogin(self):
        response = self.client.get(URL_PREPENDER + '/taxonomy/1/')

        #test we actually have an ok response
        self.assertEqual(response.status_code, 200)


    def testTaxonomyAdd(self):
        self.testLogin()

        response = self.client.post(URL_PREPENDER + '/taxonomy/add/action/',
                                    {'taxonomy_name': 'Eamonn Taxonomy', 'category_name': 'Eamonn Category',
                                     'description': 'New description'})

        taxonomy = TaxonomyItem.objects.filter(name='Eamonn Taxonomy').__getitem__(0)

        #test we actually have an ok response
        redirectURL = URL_PREPENDER + '/taxonomy/' + str(taxonomy.id) + '/'
        self.assertRedirects(response, redirectURL, status_code=302,
                             target_status_code=200)


    def testVolunteer(self):
        self.testLogin()

        response = self.client.get(URL_PREPENDER + '/volunteer')

        #test we actually have an ok response
        self.assertEqual(response.status_code, 200)


    def testContact(self):
        self.testLogin()

        response = self.client.get(URL_PREPENDER + '/contact/')

        #test we actually have an ok response
        self.assertEqual(response.status_code, 200)


    def testLogout(self):
        self.client.login(username='test', password='secret')

        response = self.client.get(URL_PREPENDER + '/accounts/logout/')
        #test we actually have an ok response
        self.assertEqual(response.status_code, 200)

        response = self.client.get(URL_PREPENDER + '/accounts/profile/')
        self.assertRedirects(response, URL_PREPENDER + '/accounts/login/?next=/accounts/profile/', status_code=302,
                             target_status_code=200)


