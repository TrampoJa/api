from django.test import TestCase
from interesses.models import Interesses
from ofertas.models import Ofertas
from users.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from freelancers.models import FreeLancers
from estabelecimentos.models import Estabelecimentos
from django.contrib.auth.models import Group


class TestInteresses(TestCase):
    def setUp(self):
        estabelecimentoGroup = Group.objects.create(name="Estabelecimento")
        freelancerGroup = Group.objects.create(name="Freelancer")

        self.client = APIClient()
        self.writer = User.objects.create_user(
            'test_user',
            'test@example.com',
            'password1'
        )
        self.writer.groups.set([freelancerGroup])
        self.writer.save()
        self.token = Token.objects.create(user=self.writer)

        self.writer2 = User.objects.create_user(
            'test2_user',
            'test2@example.com',
            'password2'
        )
        self.writer2.groups.set([estabelecimentoGroup])
        self.writer2.save()
        self.token2 = Token.objects.create(user=self.writer2)

        self.writer3 = User.objects.create_user(
            'test3_user',
            'test3@example.com',
            'password3'
        )
        self.writer3.groups.set([freelancerGroup])
        self.writer3.save()
        self.token3 = Token.objects.create(user=self.writer3)

        self.freelancer = FreeLancers(
            nome='Test',
            sobrenome='Testing',
            telefone='49999500411',
            nascimento='1997-05-25',
            bio='Piao trabaiado',
            owner=self.writer3
        )
        self.freelancer.save()

        self.estabelecimento = Estabelecimentos(
            nome='Teste',
            cnpj='09992622970',
            razao_social='TESTE',
            tipo='bodega',
            telefone='49999950411',
            owner=self.writer2
        )
        self.estabelecimento.save()

        self.oferta = Ofertas(
            nome='teste',
            valor=80,
            owner=self.writer2
        )
        self.oferta.save()
        self.interesse = Interesses(
            oferta=self.oferta,
            owner=self.writer
        )
        self.interesse.save()


class TestInteressesCreateView(TestInteresses):
    def test_create_interesses_post_sucess(self):
        data = {
            'id': self.oferta.pk
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token3.key)
        response = self.client.post("/interesse", data)
        self.assertEqual(response.status_code, 201)

    def test_create_interesses_post_error_unique(self):
        data = {
            'id': self.oferta.pk
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/interesse", data)
        self.assertEqual(response.status_code, 400)

    def test_create_interesses_post_error(self):
        data = {
            'id': 0
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/interesse", data)
        self.assertEqual(response.status_code, 404)

    def test_create_interesses_permission(self):
        data = {
            'id': self.oferta.pk
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.post("/interesse", data)
        self.assertEqual(response.status_code, 403)


class TestInteressesListToFreelancer(TestInteresses):
    def test_listToFreelancer_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get("/f_interesses/")
        self.assertEqual(response.status_code, 200)


class TestInteressesListToEstabelecimento(TestInteresses):
    def test_listToEstabelecimento_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.get("/e_interesses/")
        self.assertEqual(response.status_code, 200)
