import requests
import json
from django.core.mail import send_mail, send_mass_mail
from rest_framework.response import Response
from .base_message import BaseEmailMessage, BaseWhatsAppMessage


class SendEmailMessage(BaseEmailMessage):
    def sendWelcomeMessage(self):
        if not self.email or not self.nome:
            return False
        try:
            send_mail(
                self.titulo,
                'Esta é nossa mensagem de boas vindas. Seja Bem Vindo ' + self.nome,
                self.from_email,
                [self.email],
                fail_silently=False,
            )
            return True
        except Exception:
            return False

    def sendRecoveryMessage(self, new_password):
        if not self.email or not self.nome:
            return False
        try:
            send_mail(
                self.titulo,
                'Esta é a sua nova senha ' + new_password,
                self.from_email,
                [self.email],
                fail_silently=False,
            )
            return True
        except Exception:
            return False

    def sendNovaOfertaMessage(self):
        from django.contrib.auth.models import User
        users = User.objects.filter(last_name='Freelancer')
        emails = []
        for user in users:
            email = (
                self.titulo,
                'Um novo trampo está disponível para você.\nConfira os detalhes em https://app.trampoja.com/trampos',
                self.from_email,
                [user.email]
            )
            emails.append(email)
        """
        Implementação provisória para Wellinton
        montar lista de transmissão para envio no wpp
        """
        email = (
            self.titulo,
            'Um novo trampo está disponível para você.\nConfira os detalhes em https://app.trampoja.com/trampos',
            self.from_email,
            ['welliton_vini1999@hotmail.com']
        )
        emails.append(email)
        """
        """
        try:
            send_mass_mail(emails, fail_silently=False)
            return True
        except Exception:
            return False

    def sendInteressesMessage(self):
        if not self.email or not self.nome:
            return False
        try:
            send_mail(
                self.titulo,
                "{} acabou de demonstrar interesse na sua vaga para {}. Confira em https://app.trampoja.com/interesses"
                    .format(self.nome, self.oferta),
                self.from_email,
                [self.email],
                fail_silently=False,
            )
            return True
        except Exception:
            return False

    def sendConfirmadosMessage(self):
        if not self.email or not self.nome:
            return False
        try:
            send_mail(
                self.titulo,
                "Salve, {} acabou de confirmar o trampo para a vaga de {}. Confira em https://app.trampoja.com/confirmados"
                    .format(self.nome, self.oferta),
                self.from_email,
                [self.email],
                fail_silently=False,
            )
            return True
        except Exception:
            return False

    def sendCanceladosMessage(self):   
        if not self.email or not self.nome:
            return False
        try:
            send_mail(
                self.titulo,
                "{} acabou de cancelar o trampo para a vaga de {}. Confira em https://app.trampoja.com/confirmados"
                    .format(self.nome, self.oferta),
                self.from_email,
                [self.email],
                fail_silently=False,
            )
            return True
        except Exception:
            return False


class SendWhatsAppMessage(BaseWhatsAppMessage):
    def sendCanceladosMessage(self):   
        payload = {
            'message': "{} acabou de cancelar o trampo para a vaga de {}. Confira em https://trampoja.com/confirmados"
                .format(self.nome, self.oferta),
            'number': self.number
        }
        try:
            response = requests.post(self.url, data=json.dumps(payload), headers=self.headers)
            return Response(response)
        except Exception:
            return

    def sendInteressesMessage(self):
        payload = {
            'message': "{} acabou de demonstrar interesse na sua vaga para {}. Confira em https://trampoja.com/interesses"
                .format(self.nome, self.oferta),
            'number': self.number
        }
        try:
            response = requests.post(self.url, data=json.dumps(payload), headers=self.headers)
            return Response(response)
        except Exception:
            return

    def sendConfirmadosMessage(self):
        payload = {
            'message': "Salve, {} acabou de confirmar o trampo para a vaga de {}. Confira em https://trampoja.com/confirmados"
                .format(self.nome, self.oferta),
            'number': self.number
        }
        try:
            response = requests.post(self.url, data=json.dumps(payload), headers=self.headers)
            return Response(response)
        except Exception:
            return