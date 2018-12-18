from django.test import TestCase
from django.urls import reverse
from django.urls import resolve
from ..views import home, yards
from ..models import Yard
from django.contrib.auth.models import  User
from ..forms import NewYardForm

# Create your tests here.
class HomeTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.yard = Yard.objects.create(description="This is a test", created_by = User.objects.first())
        url = reverse('home')
        self.response = self.client.get(url)


    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        yard_url = reverse('yards', kwargs={'pk': self.yard.pk})
        self.assertContains(self.response, 'href="{0}"'.format(yard_url))

class YardTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='john', email='john@doe.com', password='123')
        Yard.objects.create(description="This is a test", created_by = User.objects.first())

    def test_yard_view_success_status_code(self):
        url = reverse('yards', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    #def test_yard_view_not_found_status_code(self):
        #url = reverse('yards', kwargs={'pk':99})
        #response = self.client.get(url)
        #self.assertEquals(response.status_code,404)

    def test_yard_url_resolves_yard_view(self):
        view = resolve('/yards/1/')
        self.assertEquals(view.func, yards)

    def test_yard_view_contains_link_back_to_homepage(self):
        yards_url = reverse('yards', kwargs={'pk' : 1})
        response = self.client.get(yards_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))

class NewYardTests(TestCase):
    def test_contains_form(self):  # <- new test
        url = reverse('new_yard')
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewYardForm)

    def test_new_yard_invalid_post_data(self):  # <- updated this one
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_yard')
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)