import io

from PIL import Image

from django.test import TestCase
from users.views import User
from estabelecimentos.models import Estabelecimentos
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


class TestEstabelecimentos(TestCase):
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

        self.estabelecimento = Estabelecimentos(
            nome='Teste',
            cnpj='09992622970',
            razao_social='TESTE',
            tipo='bodega',
            telefone='049999950411',
            owner=self.writer3
        )
        self.estabelecimento.save()

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file


class TestUploadLogo(TestEstabelecimentos):
    def test_upload_photo_sucess(self):
        photo_file = self.generate_photo_file()
        data = {
            'logo': photo_file
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token3.key)
        response = self.client.post(
            "/estabelecimento/upload/1", data, format='multipart')
        self.assertEqual(response.status_code, 200)

    def test_upload_photo_error_authentication(self):
        photo_file = self.generate_photo_file()
        data = {
            'logo': photo_file
        }
        response = self.client.post(
            "/estabelecimento/upload/1", data, format='multipart')
        self.assertEqual(response.status_code, 302)

    def test_upload_photo_error(self):
        data = {}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token3.key)
        response = self.client.post(
            "/estabelecimento/upload/1", data, format='multipart')
        self.assertEqual(response.status_code, 400)


class TestEstabelecimentosCreateView(TestEstabelecimentos):
    def test_create_estabelecimento_post_sucess(self):
        data = {
            'nome': 'Teste',
            'cnpj': '09992622972098',
            'razao_social': 'TESTE',
            'tipo': 'bodega',
            'telefone': '49999950411'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/estabelecimento/create", data)
        self.assertEqual(response.status_code, 201)

    def test_create_estabelecimento_post_error_cpfcnpj(self):
        data = {
            'nome': 'Teste',
            'cnpj': '09/*fail*/670',
            'razao_social': 'TESTE',
            'tipo': 'bodega',
            'telefone': '049999950411'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/estabelecimento/create", data)
        self.assertEqual(response.status_code, 400)

    def test_create_estabelecimento_post_error_telefone(self):
        data = {
            'nome': 'Teste',
            'cnpj': '09992622971',
            'razao_social': 'TESTE',
            'tipo': 'bodega',
            'telefone': '049/*fail*/411'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/estabelecimento/create", data)
        self.assertEqual(response.status_code, 400)

    def test_create_estabelecimento_post_error(self):
        data = {}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/estabelecimento/create", data)
        self.assertEqual(response.status_code, 400)


class TestEstabelecimentosListView(TestEstabelecimentos):
    def test_liste_estabelecimento(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get("/estabelecimento/liste")
        self.assertEqual(response.status_code, 200)


class TestEstabelecimentosProfileView(TestEstabelecimentos):
    def test_profile_estabelecimento_error(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response = self.client.get("/estabelecimento/profile")
        self.assertEqual(response.status_code, 401)

    def test_profile_estabelecimento_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token3.key)
        response = self.client.get("/estabelecimento/profile")
        self.assertEqual(response.status_code, 200)


class TestEstabelecimentosDetailView(TestEstabelecimentos):
    def test_detail_estabelecimento_error(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get("/estabelecimento/detail/0")
        self.assertEqual(response.status_code, 404)

    def test_detail_estabelecimento_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get("/estabelecimento/detail/1")
        self.assertEqual(response.status_code, 200)

    def test_detail_estabelecimento_permissions(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.get("/estabelecimento/detail/1")
        self.assertEqual(response.status_code, 200)


class TestEstabelecimentosUpdateView(TestEstabelecimentos):
    def test_update_estabelecimento_post_error(self):
        data = {}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put("/estabelecimento/update/0", data)
        self.assertEqual(response.status_code, 404)

    def test_update_estabelecimento_post_sucess(self):
        data = {
            'nome': 'Teste',
            'cnpj': '09992622970098',
            'razao_social': 'TESTE',
            'tipo': 'bodega',
            'telefone': '49999950411'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token3.key)
        response = self.client.post("/estabelecimento/update/1", data)
        self.assertEqual(response.status_code, 200)

    def test_update_estabelecimento_post_permissions(self):
        data = {
            'nome': 'Teste',
            'cnpj': '09992622970',
            'razao_social': 'TESTE',
            'tipo': 'bodega',
            'telefone': '049999950411'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.post("/estabelecimento/update/1", data)
        self.assertEqual(response.status_code, 403)


class TestEstabelecimentosDeleteView(TestEstabelecimentos):
    def test_delete_estabelecimento_error(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete("/estabelecimento/delete/0")
        self.assertEqual(response.status_code, 404)

    def test_delete_estabelecimento_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token3.key)
        response = self.client.delete("/estabelecimento/delete/1")
        self.assertEqual(response.status_code, 200)

    def test_delete_estabelecimento_permissions(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.delete("/estabelecimento/delete/1")
        self.assertEqual(response.status_code, 403)


class TestEstabelecimentosFindCNPJView(TestEstabelecimentos):
    def test_find_cnpj(self):
        data = {
            'cnpj': '19131243000197'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/estabelecimento/findCNPJ/", data)
        self.assertEqual(response.status_code, 200)

    def test_find_cnpj_error(self):
        data = {
            'cnpj': ''
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/estabelecimento/findCNPJ/", data)
        self.assertEqual(response.status_code, 400)
