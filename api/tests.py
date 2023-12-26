from django.test import TestCase
from django.urls import reverse
from .models import Task
from django.contrib.auth.models import User
from base64 import b64encode

class TaskTestCase(TestCase):
    def setUp(self):
        user = User(username='admin')
        user.set_password('1234')
        user.save()

    def test_login(self):
        auth_headers = {
            'Autorithation' : 'Basic ' +  b64encode(b'admin:1234').decode('ascii'),
        } 
        response = self.client.post('api/login',headers=auth_headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "you are loged in."})
        
    def test_create_task(self):
        auth_headers = {
            'Autorithation' : 'Basic ' +  b64encode(b'admin:1234').decode('ascii'),
        } 
        response = self.client.post('api/tasks',data={'title':'test','description':'test'},headers=auth_headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "task created."})
    def test_login_401(self):
        auth_headers = {
            'Autorithation' : 'Basic ' +  b64encode(b'admin:12345').decode('ascii'),
        } 
        response = self.client.post('api/login',headers=auth_headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"error": "noto'g'ri parol kiritdingiz"})

    

