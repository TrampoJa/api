import datetime
from django.test import TestCase
from confirmados.models import Confirmados
from ofertas.models import Ofertas
from freelancers.models import FreeLancers
from estabelecimentos.models import Estabelecimentos
from users.views import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


class TestConfirmados(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.writer = User.objects.create_user(
            'test_user',
            'test@example.com',
            'password1'
        )
        self.writer.last_name = "Estabelecimento"
        self.writer.save()
        self.token = Token.objects.create(user=self.writer)

        self.estabelecimento = Estabelecimentos(
            nome='Teste',
            cnpj='09992622970',
            razao_social='TESTE',
            tipo='bodega',
            telefone='49999950411',
            owner=self.writer
        )
        self.estabelecimento.save()

        self.writer2 = User.objects.create_user(
            'test2_user',
            'test2@example.com',
            'password2'
        )
        self.writer2.last_name = "Freelancer"
        self.writer2.save()
        self.token2 = Token.objects.create(user=self.writer2)

        self.oferta = Ofertas(
            nome='teste',
            valor=80,
            date_inicial=datetime.date.today(),
            owner=self.writer
        )
        self.oferta.save()

        self.oferta2 = Ofertas(
            nome='teste',
            valor=80,
            date_inicial=datetime.date.today(),
            status=False,
            owner=self.writer
        )
        self.oferta2.save()

        self.oferta3 = Ofertas(
            nome='teste',
            valor=80,
            date_inicial=(datetime.date.today() + datetime.timedelta(days=-1)),
            status=True,
            owner=self.writer
        )
        self.oferta3.save()

        self.confirmado = Confirmados(
            oferta=self.oferta,
            owner=self.writer
        )
        self.confirmado.save()

        self.freelancer = FreeLancers(
            nome='Test',
            sobrenome='Testing',
            telefone='499999500411',
            nascimento='1997-05-25',
            bio='Piao trabaiado',
            owner=self.writer2
        )
        self.freelancer.save()


class TestConfirmadosCreateView(TestConfirmados):
    def test_create_confirmados_post_sucess(self):
        data = {
            'freelancer': self.freelancer.pk,
            'oferta': self.oferta.pk
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/confirmado", data)
        self.assertEqual(response.status_code, 201)

    def test_create_confirmados_error_oferta_status(self):
        data = {
            'freelancer': self.freelancer.pk,
            'oferta': self.oferta2.pk
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/confirmado", data)
        self.assertEqual(response.status_code, 400)

    def test_create_confirmados_error_date(self):
        data = {
            'freelancer': self.freelancer.pk,
            'oferta': self.oferta3.pk
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/confirmado", data)
        self.assertEqual(response.status_code, 400)

    def test_create_confirmados_permission(self):
        data = {
            'freelancer': self.freelancer.pk,
            'oferta': self.oferta.pk
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.post("/confirmado", data)
        self.assertEqual(response.status_code, 403)

    def test_create_confirmados_post_error(self):
        data = {
            'freelancer': 0,
            'oferta': 0
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/confirmado", data)
        self.assertEqual(response.status_code, 404)

    def test_create_confirmados_post_error_oferta(self):
        data = {
            'freelancer': self.freelancer.pk,
            'oferta': 0
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/confirmado", data)
        self.assertEqual(response.status_code, 404)

    def test_create_confirmados_post_error_freelancer(self):
        data = {
            'freelancer': 0,
            'oferta': self.oferta2.pk
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/confirmado", data)
        self.assertEqual(response.status_code, 404)


class TestConfirmadosListToFreelancerView(TestConfirmados):
    def test_listToFreelancer_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get("/f_confirmados/")
        self.assertEqual(response.status_code, 200)


class TestConfirmadosListToEstabelecimentoView(TestConfirmados):
    def test_listToEstabelecimento_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get("/e_confirmados/")
        self.assertEqual(response.status_code, 200)
