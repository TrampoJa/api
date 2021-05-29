from datetime import date, timedelta
from re import search

from rest_framework.exceptions import ValidationError


class Validator:

    def __init__(self, data=None):
        if data is not None:
            self.telefone(data['telefone'])
            self.nascimento(data['nascimento'])

    def telefone(self, telefone):
        regex = r'[^\d]'
        if search(regex, telefone):
            raise ValidationError(detail='Informe um telefone válido.')

        lenght = len(telefone)
        if lenght < 10 or lenght > 11:
            raise ValidationError(detail='Informe um telefone válido.')

    def nascimento(self, nascimento):
        time = date.today() + timedelta(weeks=-834)  # 16 years
        if nascimento >= time:
            raise ValidationError(detail='Você precisa ter mais que 16 anos.')
