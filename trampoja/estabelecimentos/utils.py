from django.http import *
import datetime
from django.utils import timezone

class Utils:

    def validator(data):
        telefone = data['telefone']
        cpf_cnpj = data['cpf_cnpj']

        if not telefone.isdecimal():
            raise Http404
        if not cpf_cnpj.isdecimal():
            raise Http404