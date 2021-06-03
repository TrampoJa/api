from trampoja.celery import app
from mensagens.send_messages import SendEmailMessage


@app.task
def task_send_nova_oferta_message():
    SendEmailMessage()\
        .sendNovaOfertaMessage()
