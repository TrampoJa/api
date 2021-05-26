import re
from rest_framework.exceptions import ValidationError


class Utils:

    def password_validator(self, password):
        if len(password) < 6:
            raise ValidationError(detail='Senha inválida.')

    def email_validator(self, email):
        regex = '^[\w\.-]+@(?:[\w-]+\.)+[\w-]{2,4}$'
        if not re.search(regex, email):
            raise ValidationError(detail='Email inválido')

    def validator(self, email, password):
        self.password_validator(password)
        self.email_validator(email)
