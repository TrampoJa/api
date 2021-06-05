from rest_framework.exceptions import ValidationError
from re import search


class Validator:

    def __init__(self, data):
        for field in data:
            method = getattr(self, field)
            method(data[field])

    def password(self, password):
        if len(password) < 6:
            raise ValidationError(detail='Senha inválida.')

    def email(self, email):
        regex = r'^[\w_.+-]+@[\w-]+\.[\w.-]+$'
        if not search(regex, email):
            raise ValidationError(detail='Email inválido.')

    def first_name(self, first_name):
        regex = r'([^A-Za-z\s])'

        if search(regex, first_name):
            raise ValidationError(detail='Primeiro nome inválido.')

    def last_name(self, last_name):
        regex = r'([^A-Za-z\s])'
        if search(regex, last_name):
            raise ValidationError(detail='Ultimo nome inválido.')

    def username(self, username):
        ...
