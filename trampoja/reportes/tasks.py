from trampoja.celery import app
from mensagens.send_messages import SendEmailMessage


@app.task
def task_send_reportes_message():
    SendEmailMessage()\
        .sendReportesMessage()
