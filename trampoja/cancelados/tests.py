import datetime
from datetime import timedelta
from django.test import TestCase
from cancelados.models import Cancelados
from ofertas.models import Ofertas
from freelancers.models import FreeLancers
from estabelecimentos.models import Estabelecimentos
from confirmados.models import Confirmados
from users.views import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.http import *


class TestCancelados(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.writer = User.objects.create_user(
            'test_user',
            'test@example.com', 
            'password1'
        )
        self.writer.last_name = 'Estabelecimento'
        self.writer.save()
        self.token = Token.objects.create(user=self.writer)

        self.writer2 = User.objects.create_user(
            'test2_user',
            'test2@example.com', 
            'password2'
        )
        self.writer2.last_name = 'Freelancer' 
        self.writer2.save()
        self.token2 = Token.objects.create(user=self.writer2)

        self.writer3 = User.objects.create_user(
            'test3_user',
            'test3@example.com', 
            'password3'
        )
        self.writer3.save()
        self.token3 = Token.objects.create(user=self.writer3)

        self.estabelecimento = Estabelecimentos(
            nome = 'Teste',
            cpf_cnpj = '09992622970',
            razao_social = 'TESTE',
            tipo = 'bodega',
            telefone = '049999950411',
            owner = self.writer
        )
        self.estabelecimento.save()
        
        self.hora = datetime.datetime.now() + timedelta(hours=7)
        self.oferta = Ofertas(
            nome = 'teste',
            valor = 80,
            date_inicial = datetime.date.today(),
            time = self.hora.time(),
            owner = self.writer
        )
        self.oferta.save()

        self.hora_limite = datetime.datetime.now() + timedelta(hours=5)
        self.oferta2 = Ofertas(
            nome = 'teste',
            valor = 80,
            date_inicial = datetime.date.today(),
            time = self.hora_limite.time(),
            owner = self.writer
        )
        self.oferta2.save()

        self.oferta3 = Ofertas(
            nome = 'teste',
            valor = 80,
            date_inicial = (datetime.date.today() + datetime.timedelta(days=-1)),
            status = True,
            owner = self.writer
        )
        self.oferta3.save()

        self.freelancer = FreeLancers(
            nome = 'Test',
            sobrenome = 'Testing',
            telefone = '499999500411',
            nascimento = '1997-05-25',
            bio = 'Piao trabaiado',
            owner = self.writer2
        )
        self.freelancer.save()

        self.confirmado = Confirmados(
            oferta = self.oferta,
            owner = self.writer2
        )
        self.confirmado.save()


class TestCanceladosCreateView(TestCancelados):   
    def test_create_cancelados_post_sucess(self):
        data = {
            'freelancer': self.freelancer.pk,
            'oferta': self.oferta.pk,
            'confirmado': self.confirmado.pk,
            'justificativa': 'teste'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)    
        response = self.client.post("/cancelar", data)
        self.assertEqual(response.status_code, 201)

    def test_create_cancelados_post_error_hora_limite(self):
        data = {
            'freelancer': self.freelancer.pk,
            'oferta': self.oferta2.pk,
            'confirmado': self.confirmado.pk,
            'justificativa': 'teste'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)    
        response = self.client.post("/cancelar", data)
        self.assertEqual(response.status_code, 400)

    def test_create_cancelados_post_error_date(self):
        data = {
            'freelancer': self.freelancer.pk,
            'oferta': self.oferta3.pk,
            'confirmado': self.confirmado.pk,
            'justificativa': 'teste'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)    
        response = self.client.post("/cancelar", data)
        self.assertEqual(response.status_code, 400)

    def test_create_cancelados_post_error_confirmado(self):
        data = {
            'freelancer': self.freelancer.pk,
            'oferta': self.oferta.pk,
            'confirmado': 0,
            'justificativa': 'teste'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)    
        response = self.client.post("/cancelar", data)
        self.assertEqual(response.status_code, 404)

    def test_create_cancelados_post_error_permission(self):
        data = {
            'freelancer': self.freelancer.pk,
            'oferta': self.oferta.pk,
            'confirmado': self.confirmado.pk,
            'justificativa': 'teste'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token3.key)    
        response = self.client.post("/cancelar", data)
        self.assertEqual(response.status_code, 403)


class TestCanceladosListToFreelancerView(TestCancelados):
    def test_listToFreelancer_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)    
        response = self.client.get("/f_cancelados/")
        self.assertEqual(response.status_code, 200)


class TestCanceladosListToEstabelecimentoView(TestCancelados):
    def test_listToEstabelecimento_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.get("/e_cancelados/")
        self.assertEqual(response.status_code, 200)