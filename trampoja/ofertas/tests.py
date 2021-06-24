import datetime

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from ofertas.models import Ofertas

from django.contrib.auth.models import User

from estabelecimentos.models import Estabelecimentos


class TestOfertas(TestCase):
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

        self.oferta = Ofertas(
            nome='teste',
            valor=80,
            owner=self.writer
        )
        self.oferta.save()
        self.date = datetime.date.today()

        self.oferta2 = Ofertas(
            nome='teste',
            valor=80,
            owner=self.writer,
            edit=False
        )
        self.oferta2.save()
        self.date = datetime.date.today()

        self.estabelecimento = Estabelecimentos(
            nome='Teste',
            cnpj='09992622970',
            razao_social='TESTE',
            tipo='bodega',
            telefone='049999950411',
            ofertas_para_publicar=1,
            owner=self.writer
        )
        self.estabelecimento.save()

        self.estabelecimento2 = Estabelecimentos(
            nome='Teste',
            cnpj='09992622971',
            razao_social='TESTE',
            tipo='bodega',
            telefone='049999950411',
            ofertas_para_publicar=0,
            owner=self.writer2
        )
        self.estabelecimento2.save()


class TestOfertasCreateView(TestOfertas):
    def test_create_ofertas_post_sucess(self):
        data = {
            'nome': 'Garcom',
            'valor': 10,
            'time': '18:00',
            'date_inicial': self.date,
            'obs': 'Chegar 10 minutos antes do horário',
            'freelancers': 1
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/ofertas/create", data)
        self.assertEqual(response.status_code, 201)

    def test_create_ofertas_post_sucess_muitas(self):
        data = {
            'nome': 'Garcom',
            'valor': 10,
            'time': '18:00',
            'date_inicial': self.date,
            'obs': 'Chegar 10 minutos antes do horário',
            'freelancers': 3
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/ofertas/create", data)
        self.assertEqual(response.status_code, 201)

    def test_create_ofertas_post_error_valor(self):
        data = {
            'nome': 'Garcom',
            'valor': 9,
            'time': '18:00',
            'date_inicial': self.date,
            'obs': 'Chegar 10 minutos antes do horário',
            'freelancers': 1
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/ofertas/create", data)
        self.assertEqual(response.status_code, 400)

    def test_create_ofertas_post_error_date(self):
        data = {
            'nome': 'Garcom',
            'valor': 50,
            'time': '18:00',
            'date_inicial': self.date + datetime.timedelta(days=-1),
            'obs': 'Chegar 10 minutos antes do horário',
            'freelancers': 1
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/ofertas/create", data)
        self.assertEqual(response.status_code, 400)

    def test_create_ofertas_post_error_ofertas_para_publicar(self):
        data = {
            'nome': 'Garcom',
            'valor': 50,
            'time': '18:00',
            'date_inicial': self.date,
            'obs': 'Chegar 10 minutos antes do horário',
            'freelancers': 1
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.post("/ofertas/create", data)
        self.assertEqual(response.status_code, 400)

    def test_create_ofertas_post_error(self):
        data = {
            'nome': '',
            'valor': '',
            'time': '',
            'date_inicial': '',
            'obs': '',
            'date_final': '',
            'freelancers': '0'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/ofertas/create", data)
        self.assertEqual(response.status_code, 400)

    def test_create_ofertas_post_error_authenticate(self):
        data = {
            'nome': '',
            'valor': '',
            'time': '',
            'date_inicial': '',
            'obs': '',
            'date_final': '',
            'freelancers': '0'
        }
        response = self.client.post("/ofertas/create", data)
        self.assertEqual(response.status_code, 302)


class TestOfertasListView(TestOfertas):
    def test_liste_ofertas(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get("/ofertas/liste")
        self.assertEqual(response.status_code, 200)

    def test_liste_ofertas_error_authenticate(self):
        response = self.client.get("/ofertas/liste")
        self.assertEqual(response.status_code, 302)


class TestOfertasProfileView(TestOfertas):
    def test_profile_ofertas_error(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response = self.client.get("/ofertas/profile")
        self.assertEqual(response.status_code, 401)

    def test_profile_ofertas_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get("/ofertas/profile")
        self.assertEqual(response.status_code, 200)


class TestOfertasDetailView(TestOfertas):
    def test_detail_ofertas_error(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get("/ofertas/detail/0")
        self.assertEqual(response.status_code, 404)

    def test_detail_ofertas_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get("/ofertas/detail/1")
        self.assertEqual(response.status_code, 200)

    def test_detail_ofertas_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.get("/ofertas/detail/1")
        self.assertEqual(response.status_code, 200)


class TestOfertasUpdateView(TestOfertas):
    def test_update_ofertas_post_error(self):
        data = {
            'nome': '',
            'valor': '',
            'time': '',
            'date_inicial': '',
            'date_final': '',
            'obs': ''
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put("/ofertas/update/0", data)
        self.assertEqual(response.status_code, 404)

    def test_update_ofertas_post_sucess(self):
        data = {
            'nome': 'Garcom',
            'valor': 100,
            'time': '18:00',
            'date_inicial': self.date,
            'obs': 'Chegar 10 minutos antes do horário',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/ofertas/update/1", data)
        self.assertEqual(response.status_code, 200)

    def test_update_ofertas_edit_error(self):
        data = {
            'nome': 'Garcom',
            'valor': 100,
            'time': '18:00',
            'date_inicial': self.date,
            'obs': 'Chegar 10 minutos antes do horário',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/ofertas/update/2", data)
        self.assertEqual(response.status_code, 400)

    def test_update_ofertas_permission(self):
        data = {
            'nome': 'Garcom',
            'valor': 100,
            'time': '18:00',
            'date_inicial': self.date,
            'obs': 'Chegar 10 minutos antes do horário',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.post("/ofertas/update/1", data)
        self.assertEqual(response.status_code, 403)


class TestOfertasDeleteView(TestOfertas):
    def test_delete_ofertas_error(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete("/ofertas/delete/0")
        self.assertEqual(response.status_code, 404)

    def test_delete_ofertas_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete("/ofertas/delete/1")
        self.assertEqual(response.status_code, 200)

    def test_delete_ofertas_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.delete("/ofertas/delete/1")
        self.assertEqual(response.status_code, 403)
