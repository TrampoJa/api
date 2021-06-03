from trampoja.celery import app
from mensagens.send_messages import SendEmailMessage


@app.task
def task_send_welcome_message(email, nome):
    SendEmailMessage(email=email, nome=nome)\
        .sendWelcomeMessage()


@app.task
def task_send_recovery_message(email, nome, new_password):
    SendEmailMessage(email=email, nome=nome)\
        .sendRecoveryMessage(new_password)
