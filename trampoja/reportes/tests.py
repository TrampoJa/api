from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from .models import Reportes, Motivos

from ofertas.models import Ofertas

from users.models import User

from estabelecimentos.models import Estabelecimentos

from freelancers.models import FreeLancers


class TestReportes(TestCase):
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
            'luizdendena@trampoja.com',
            'password1'
        )
        self.token2 = Token.objects.create(user=self.writer2)

        self.writer3 = User.objects.create_user(
            'test_user3',
            'test@trampoja.com',
            'password1'
        )
        self.token3 = Token.objects.create(user=self.writer3)

        self.oferta = Ofertas(
            nome='Oferta Teste',
            valor=80,
            owner=self.writer,
            closed = True
        )
        self.oferta.save()

        self.oferta2 = Ofertas(
            nome='Oferta Teste',
            valor=80,
            owner=self.writer,
            closed = False
        )
        self.oferta2.save()

        self.estabelecimento = Estabelecimentos(
            nome='Empresa Teste',
            cnpj='09992622970',
            razao_social='TESTE',
            tipo='bodega',
            telefone='049999950411',
            owner=self.writer
        )
        self.estabelecimento.save()

        self.freelancer = FreeLancers(
            nome='Test',
            sobrenome='Freela Teste',
            telefone='499999500411',
            nascimento='1997-05-25',
            bio='Piao trabaiado',
            owner=self.writer2
        )
        self.freelancer.save()

        self.freelancer2 = FreeLancers(
            nome='Test',
            sobrenome='Freela Teste',
            telefone='499999500411',
            nascimento='1997-05-25',
            bio='Piao trabaiado',
            owner=self.writer3
        )
        self.freelancer2.save()

        self.reporte = Reportes(
            freelancer=self.freelancer2,
            trampo=self.oferta2,
            descricao='Teste'
        )
        self.reporte.save()

        self.motivo = Motivos(
            motivo=1,
            nome='Motivo Teste'
        )
        self.motivo.save()

        self.motivo2 = Motivos(
            motivo=2,
            nome='Motivo2 Teste'
        )
        self.motivo2.save()


class TestCreateReportesView(TestReportes):
    def test_create_reporte_post_sucess(self):
        data = {
            'freelancer': self.freelancer.id,
            'oferta': self.oferta.id,
            'descricao': 'Descricao teste',
            'motivos': {
                1: True,
                2: True
            }
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/reportar", format='json', data=data)
        self.assertEqual(response.status_code, 201)

    def test_create_reporte_post_error_unique(self):
        data = {
            'freelancer': self.freelancer2.id,
            'oferta': self.oferta2.id,
            'descricao': 'Descricao teste',
            'motivos': {
                1: True,
                2: True
            }
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/reportar", format='json', data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_reporte_post_error_oferta_not_closed(self):
        data = {
            'freelancer': self.freelancer.id,
            'oferta': self.oferta2.id,
            'descricao': 'Descricao teste',
            'motivos': {
                1: True,
                2: True
            }
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/reportar", format='json', data=data)
        self.assertEqual(response.status_code, 400)


class TestRepostesGetView(TestReportes):
    def test_get_reportes(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get("/reportes/1")
        self.assertEqual(response.status_code, 200)