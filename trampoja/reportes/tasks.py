from trampoja.celery import app
from mensagens.send_messages import SendEmailMessage


@app.task
def task_send_reportes_message(email, nome, oferta, motivos, descricao):
    SendEmailMessage(email=email, nome=nome, oferta=oferta)\
        .sendReportesMessage(motivos, descricao)
