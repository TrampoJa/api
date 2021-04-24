import os
import io

from PIL import Image

from django.test import TestCase
from users.views import User
from freelancers.models import FreeLancers
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.http import *
import datetime


class TestFreeLancers(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.writer = User.objects.create_user(
            'test_user',
            'test@example.com', 
            'password1'
        )
        self.token = Token.objects.create(user=self.writer)

        self.writer2 = User.objects.create_user(
            'test_user2',
            'test2@example.com', 
            'password1'
        )
        self.token2 = Token.objects.create(user=self.writer2)

        self.writer3 = User.objects.create_user(
            'test_user3',
            'test3@example.com', 
            'password1'
        )
        self.token3 = Token.objects.create(user=self.writer3)

        self.freelancer = FreeLancers(
            nome = 'Test',
            sobrenome = 'Testing',
            telefone = '499999500411',
            nascimento = '1997-05-25',
            bio = 'Piao trabaiado',
            owner = self.writer3
        )
        self.freelancer.save()

        self.date = datetime.date.today()

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file


class TestUploadFoto(TestFreeLancers):
    def test_upload_photo_sucess(self):
        photo_file = self.generate_photo_file()
        data = {
            'foto':photo_file
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token3.key)
        response = self.client.post("/freelancer/upload/1", data, format='multipart')
        self.assertEqual(response.status_code, 200)
    
    def test_upload_photo_error_authentication(self):
        photo_file = self.generate_photo_file()
        data = {
            'foto':photo_file
        }
        response = self.client.post("/freelancer/upload/1", data, format='multipart')
        self.assertEqual(response.status_code, 403)
    
    def test_upload_photo_error(self):
        photo_file = self.generate_photo_file()
        data = {}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token3.key)
        response = self.client.post("/freelancer/upload/1", data, format='multipart')
        self.assertEqual(response.status_code, 400)


class TestFreeLancersCreateView(TestFreeLancers):
    def test_create_freelancer_post_sucess(self):
        data = {
            'nome': 'Test',
            'sobrenome': 'Testing',
            'telefone': '499999500411',
            'nascimento': '1997-05-25',
            'bio': 'Piao trabaiado',
            'rg': '1456987'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/freelancer/create", data)
        self.assertEqual(response.status_code, 201)

    def test_create_freelancer_post_error_telefone(self):
        data = {
            'nome': 'Test',
            'sobrenome': 'Testing',
            'telefone': '4999*fail*11',
            'nascimento': '1997-05-25',
            'bio': 'Piao trabaiado',
            'rg': '1456987'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/freelancer/create", data)
        self.assertEqual(response.status_code, 400)
    
    def test_create_freelancer_post_error_nascimento(self):
        data = {
            'nome': 'Test',
            'sobrenome': 'Testing',
            'telefone': '499999500411',
            'nascimento': self.date + datetime.timedelta(weeks=-782), # 15 years
            'bio': 'Piao trabaiado',
            'rg': '1456987'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/freelancer/create", data)
        self.assertEqual(response.status_code, 400)

    def test_create_freelancer_post_error(self):
        data = {}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/freelancer/create", data)
        self.assertEqual(response.status_code, 400)


class TestFreeLancersListView(TestFreeLancers):
    def test_liste_freelancer(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get("/freelancer/liste")
        self.assertEqual(response.status_code, 200)


class TestFreeLancersProfileView(TestFreeLancers):
    def test_profile_freelancer_error(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response = self.client.get("/freelancer/profile")
        self.assertEqual(response.status_code, 401)
 
    def test_profile_freelancer_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token3.key)
        response = self.client.get("/freelancer/profile")
        self.assertEqual(response.status_code, 200)


class TestFreeLancersDetailiew(TestFreeLancers):
    def test_detail_freelancer_error(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get("/freelancer/detail/0")
        self.assertEqual(response.status_code, 404)
 
    def test_detail_freelancer_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get("/freelancer/detail/1")
        self.assertEqual(response.status_code, 200)

    def test_detail_freelancer_permissions_safe_methods(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.get("/freelancer/detail/1")
        self.assertEqual(response.status_code, 200)


class TestFreeLancersUpdateView(TestFreeLancers):
    def test_update_freelancer_post_error(self):
        data = {}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put("/freelancer/update/0", data)
        self.assertEqual(response.status_code, 404)

    def test_update_freelancer_post_sucess(self):
        data = {
            'nome': 'Test',
            'sobrenome': 'Testing',
            'telefone': '499999500411',
            'nascimento': '1997-05-25',
            'bio': 'Piao trabaiado',
            'rg': '1456987'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token3.key)
        response = self.client.post("/freelancer/update/1", data)
        self.assertEqual(response.status_code, 200)

    def test_update_freelancer_post_permissions(self):
        data = {
            'nome': 'Test',
            'sobrenome': 'Testing',
            'telefone': '499999500411',
            'nascimento': '1997-05-25',
            'bio': 'Piao trabaiado',
            'rg': '1456987'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.post("/freelancer/update/1", data)
        self.assertEqual(response.status_code, 403)


class TestFreeLancersDeleteView(TestFreeLancers):
    def test_delete_freelancer_error(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete("/freelancer/delete/0")
        self.assertEqual(response.status_code, 404)

    def test_delete_freelancer_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token3.key)
        response = self.client.delete("/freelancer/delete/1")
        self.assertEqual(response.status_code, 200)

    def test_delete_freelancer_permissions_error(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.delete("/freelancer/delete/1")
        self.assertEqual(response.status_code, 403)


class TestCountOfertasConfirmadasFreelancerView(TestFreeLancers):
    def test_count_ofertas_freelancer_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token3.key)
        response = self.client.get("/freelancer/count-ofertas")
        self.assertEqual(response.status_code, 200)

    def test_count_ofertas_freelancer_authentication_error(self):
        response = self.client.get("/freelancer/count-ofertas")
        self.assertEqual(response.status_code, 404)


class TestHistoricoFreelancerView(TestFreeLancers):
    def test_historico_freelancer_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token3.key)
        response = self.client.get("/freelancer/historico/3")
        self.assertEqual(response.status_code, 200)

    def test_historico_freelancer_not_found_error(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get("/freelancer/historico/0")
        self.assertEqual(response.status_code, 400)