from rest_framework.exceptions import ValidationError
from re import compile, search, sub


class Validator:

    def __init__(self, data=None):
        if data is not None:
            self.password(data['password'])
            self.email(data['email'])
            self.name(data['first_name'], data['last_name'])

    def password(self, password):
        if len(password) < 6:
            raise ValidationError(detail='Senha inválida.')

    def email(self, email):
        regex = r'^[\w_.+-]+@[\w-]+\.[\w.-]+$'
        if not search(regex, email):
            raise ValidationError(detail='Email inválido.')

    def name(self, first_name, last_name):
        regex = compile(r'([^A-Za-z\s])')

        if regex.search(first_name):
            raise ValidationError(detail='Primeiro nome inválido.')

        if regex.search(last_name):
            raise ValidationError(detail='Ultimo nome inválido.')


class Formater:

    def name(self, data):
        fullName = data['first_name'] + ' ' + data['last_name']
        regex = r'\s+'
        fullName = sub(regex, ' ', fullName)
        fullName = fullName.strip()
        return fullName
