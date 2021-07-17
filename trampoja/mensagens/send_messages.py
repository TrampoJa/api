import requests
import json
from django.core.mail import send_mail, send_mass_mail, mail_admins
from rest_framework.response import Response
from .base_message import BaseEmailMessage, BaseWhatsAppMessage


class SendEmailMessage(BaseEmailMessage):
    def sendWelcomeMessage(self):
        if not self.email or not self.nome:
            return False
        try:
            send_mail(
                self.titulo,
                f'Bem vindo ao Trampo Já! {self.nome,}\n'
                f'A gente fica muito feliz de ter você com a gente, afinal nosso objetivo é simplificar sua vida.\n'
                f'Estamos totalmente a disposição pra tirar qualquer dúvida, para qualquer informação, é só chamar a gente, combinado?\n'
                f'Então é isso, bora trampar!\n\n'
                f'Trampo? Já!\n',
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
                'Esta é a sua nova senha provisória: ' + new_password,
                self.from_email,
                [self.email],
                fail_silently=False,
            )
            return True
        except Exception:
            return False

    def sendNovaOfertaMessage(self):
        from users.models import User
        users = User.objects.filter(groups__name='Freelancer')
        emails = []

        mail_admins(
            self.titulo,
            'Um novo trampo está disponível.',
        )

        for user in users:
            email = (
                self.titulo,
                f'Tem trampo novo no feed, corre lá e tenta a sorte!\n'
                f'Pra conferir é só clicar no link https://app.trampoja.com/trampos\n'
                f'Bora bora bora!\n\n'
                f'Trampo? Já!\n',
                self.from_email,
                [user.email]
            )
            emails.append(email)

        try:
            send_mass_mail(emails, fail_silently=True)
            return True
        except Exception:
             return False

    def sendInteressesMessage(self):
        if not self.email or not self.nome:
            return False
        try:
            send_mail(
                self.titulo,
                f'O freelancer {self.nome} demonstrou interesse na vaga que você disponibilizou para {self.oferta}.\n'
                f'Confirme o quanto antes para que tanto você quanto ele consigam se organizar melhor\n'
                f'Para confirmar acesse: https://app.trampoja.com/interesses \n\n'
                f'Trampo? Já!\n',
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
                f'Booooa!\n'
                f'Seu trampo foi confirmado com o {self.nome} para a vaga de {self.oferta}.\n'
                f'Só pra reforçar, não esqueça de conferir as informações da vaga em: https://app.trampoja.com/confirmados \n\n'
                f'Vale lembrar que você NÃO PODE VACILAR E NÃO IR, afinal vai constar no\n'
                f'seu histórico e com 2 furadas sem justificativa a gente não vai ter como\n'
                f'arrumar mais trampos pra você :( .\n\n'
                f'Trampo? Já!\n',
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
                f'A gente lamenta informar mas {self.nome} cancelou com você!\n'
                f'Pedimos desculpas pelo inconveniente.\n'
                f'Caso queira, pode conferir a justificativa do cancelamento em: https://app.trampoja.com/cancelados.\n\n'
                f'Com carinho, equipe TrampoJá.\n',
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
            response = requests.post(
                self.url, data=json.dumps(payload), headers=self.headers)
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
            response = requests.post(
                self.url, data=json.dumps(payload), headers=self.headers)
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
            response = requests.post(
                self.url, data=json.dumps(payload), headers=self.headers)
            return Response(response)
        except Exception:
            return
