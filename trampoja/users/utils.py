import re
from django.http import *
from rest_framework.exceptions import ValidationError


class Utils:

    def password_validator(self, password):
        if len(password) < 6:
            raise ValidationError(detail="Senha inválida.")

    def email_validator(self, email):
        regex_com = '^[a-z0-9]+[\._]?[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        regex_com_br = '^[a-z0-9]+[\._]?[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}\w+[.]\w{2,3}$'
        if re.search(regex_com, email) or re.search(regex_com_br, email):
            pass
        else:    
            raise ValidationError(detail="Email inválido")

    def validator(self, email, password):
        self.password_validator(password)
        self.email_validator(email)