import re
from django.http import regex_com_br
from rest_framework.exceptions import ValidationError


class Utils:

    def password_validator(self, password):
        if len(password) < 6:
            raise ValidationError(detail='Senha inválida.')

    def email_validator(self, email):
        regex_com = '^[\w\.-]+@(?:[\w-]+\.)+[\w-]{2,4}$'
        if re.search(regex_com, email) or re.search(regex_com_br, email):
            pass
        else:
            raise ValidationError(detail='Email inválido')

    def validator(self, email, password):
        self.password_validator(password)
        self.email_validator(email)
