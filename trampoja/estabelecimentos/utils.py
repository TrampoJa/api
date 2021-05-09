import datetime

from django.http import *
from django.utils import timezone

from rest_framework.exceptions import ValidationError

class Utils:

    def validator(data):
        telefone = data['telefone']
        cpf_cnpj = data['cpf_cnpj']

        if not telefone.isdecimal():
            raise ValidationError(detail="Informe um telefone válido.")
        if not cpf_cnpj.isdecimal():
            raise ValidationError(detail="Informe um cpf ou cnpj válido.")