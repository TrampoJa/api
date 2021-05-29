from rest_framework.exceptions import ValidationError
from re import search


class Validator:

    def __init__(self, data=None):
        if data is not None:
            self.password(data['password'])
            self.email(data['email'])

    def password(self, password):
        if len(password) < 6:
            raise ValidationError(detail='Senha inválida.')

    def email(self, email):
        regex = r'^[\w\.-]+@(?:[\w-]+\.)+[\w-]{2,4}$'
        if not search(regex, email):
            raise ValidationError(detail='Email inválido')


class Formater:
    pass

# first name && last name
