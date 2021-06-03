from django.test import TestCase
from .send_messages import *


class TestEmailMessages(TestCase):
    def setUp(self):
        self.nome = 'Teste'
        self.email = 'teste@teste.com'
        self.oferta = 'Garçom'


class TestWelcomeMessage(TestEmailMessages):
    def test_send_welcome_message_succes(self):
        response = SendEmailMessage(nome=self.nome, email=self.email)\
            .sendWelcomeMessage()
        self.assertEqual(response, True)

    def test_send_welcome_message_error_nome(self):
        response = SendEmailMessage(nome=None, email=self.email)\
            .sendWelcomeMessage()
        self.assertEqual(response, False)

    def test_send_welcome_message_error_email(self):
        response = SendEmailMessage(nome=self.nome, email=None)\
            .sendWelcomeMessage()
        self.assertEqual(response, False)


class TestRecoveryMessage(TestEmailMessages):
    def test_send_recovery_message_succes(self):
        response = SendEmailMessage(nome=self.nome, email=self.email)\
            .sendWelcomeMessage()
        self.assertEqual(response, True)

    def test_send_recovery_message_error_nome(self):
        response = SendEmailMessage(nome=None, email=self.email)\
            .sendWelcomeMessage()
        self.assertEqual(response, False)

    def test_send_recovery_message_error_email(self):
        response = SendEmailMessage(nome=self.nome, email=None)\
            .sendWelcomeMessage()
        self.assertEqual(response, False)


class TestNovaOfertaMessage(TestEmailMessages):
    def test_send_nova_oferta_message_succes(self):
        response = SendEmailMessage()\
            .sendNovaOfertaMessage()
        self.assertEqual(response, True)


class TestInteressesMessage(TestEmailMessages):
    def test_send_interesse_message_succes(self):
        response = SendEmailMessage(nome=self.nome, email=self.email, oferta=self.oferta)\
            .sendInteressesMessage()
        self.assertEqual(response, True)

    def test_send_interesse_message_error_nome(self):
        response = SendEmailMessage(nome=None, email=self.email, oferta=self.oferta)\
            .sendInteressesMessage()
        self.assertEqual(response, False)

    def test_send_interesse_message_error_email(self):
        response = SendEmailMessage(nome=self.nome, email=None, oferta=self.oferta)\
            .sendInteressesMessage()
        self.assertEqual(response, False)


class TestConfirmadosMessage(TestEmailMessages):
    def test_send_confirmadi_message_succes(self):
        response = SendEmailMessage(nome=self.nome, email=self.email, oferta=self.oferta)\
            .sendConfirmadosMessage()
        self.assertEqual(response, True)

    def test_send_confirmado_message_error_nome(self):
        response = SendEmailMessage(nome=None, email=self.email, oferta=self.oferta)\
            .sendConfirmadosMessage()
        self.assertEqual(response, False)

    def test_send_confirmado_message_error_email(self):
        response = SendEmailMessage(nome=self.nome, email=None, oferta=self.oferta)\
            .sendConfirmadosMessage()
        self.assertEqual(response, False)


class TestCanceladosMessage(TestEmailMessages):
    def test_send_cancelado_message_succes(self):
        response = SendEmailMessage(nome=self.nome, email=self.email, oferta=self.oferta)\
            .sendCanceladosMessage()
        self.assertEqual(response, True)

    def test_send_cancelado_message_error_nome(self):
        response = SendEmailMessage(nome=None, email=self.email, oferta=self.oferta)\
            .sendCanceladosMessage()
        self.assertEqual(response, False)

    def test_send_cancelado_message_error_email(self):
        response = SendEmailMessage(nome=self.nome, email=None, oferta=self.oferta)\
            .sendCanceladosMessage()
        self.assertEqual(response, False)
