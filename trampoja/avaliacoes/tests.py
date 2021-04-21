import datetime
from django.test import TestCase
from avaliacoes.models import Avaliacoes
from users.views import User
from rest_framework.test import APIClient
from django.http import *
from ofertas.models import Ofertas
from rest_framework.authtoken.models import Token


class TestAvaliacoes(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.writer = User.objects.create_user(
            'test_user',
            'test@example.com', 
            'password1'
        )
        self.token = Token.objects.create(user=self.writer)

        self.writer2 = User.objects.create_user(
            'test2_user',
            'test2@example.com', 
            'password2'
        )
        
        self.oferta = Ofertas(
            nome = 'teste',
            valor = 80,
            date_inicial = datetime.date.today(),
            owner = self.writer
        )
        self.oferta.save()
        
        self.oferta2 = Ofertas(
            nome = 'teste',
            valor = 80,
            date_inicial = datetime.date.today(),
            owner = self.writer
        )
        self.oferta2.save()

        self.avaliacao = Avaliacoes(
            nota = 4,
            owner = self.writer,
            oferta = self.oferta
        )
        self.avaliacao.save()


class TestAvaliacoesCreateView(TestAvaliacoes):
    def test_create_avaliacao_post_sucess(self):
        data ={
            'owner': self.writer2.pk,
            'oferta': self.oferta2.pk,
            'nota': 4
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)    
        response = self.client.post("/avaliacao", data)
        self.assertEqual(response.status_code, 201)

    def test_create_avaliacao_post_error_unique(self):
        data ={
            'owner': self.writer.pk,
            'oferta': self.oferta.pk,
            'nota': 4
        }    
        response = self.client.post("/avaliacao", data)
        self.assertEqual(response.status_code, 400)
    
    def test_create_avaliacao_post_error(self):
        data ={
            'owner': 0,
            'oferta': 0,
            'nota': ''
        }    
        response = self.client.post("/avaliacao", data)
        self.assertEqual(response.status_code, 404)


class TestAvaliacoesGetSelfView(TestAvaliacoes):
    def test_getSelf_avaliacao_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)    
        response = self.client.get("/avaliacao/get")
        self.assertEqual(response.status_code, 200)