from django.test import TestCase
from django.urls import reverse
import json
# Create your tests here.
from accounts.models import ApplicationStatus, JobApplication, Profile, JobPostDetail
from django.contrib.auth.models import User

class LoginViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser1', 'password': '1X<ISRUkw+tuK'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/dashboard')

class RegisterViewTest(TestCase):
    def test_register(self):
        response = self.client.post(reverse('register'), {'first_name': 'firstname', 
        'last_name': 'lastname','username': 'usernametest','email': 'test@test.com','password': '123456'
        , 'password2': '123456'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login')        

class AddJobApplicationViewTest(TestCase):
    def setUp(self):
        status = ApplicationStatus.objects.create(pk=1, value='N/A')
        status.save()
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')

    def test_add_job_application(self):
        response = self.client.post(reverse('addJobApplication'), json.dumps({"job_title":"test","company":"testcompany","applicationdate":"2018-01-01","status":"1","source":"testsource"}),content_type='application/json')
        self.assertEqual(response.status_code, 200)      

class ProfileViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')

    def test_open_profile(self):
        response = self.client.post(reverse('profile'))
        self.assertEqual(response.status_code, 200)           