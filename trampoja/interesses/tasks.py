from trampoja.celery import app
from mensagens.send_messages import SendEmailMessage, SendWhatsAppMessage


@app.task
def task_send_interesse_message(email, nome, oferta):
    SendEmailMessage(email=email, nome=nome, oferta=oferta)\
        .sendInteressesMessage()
