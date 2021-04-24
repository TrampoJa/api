import datetime

from django.http import *
from django.utils import timezone

from rest_framework.exceptions import ValidationError


class Utils:

    def validator(data):
        telefone = data['telefone']
        nascimento = data['nascimento']
        time = datetime.date.today() + datetime.timedelta(weeks=-834) # 16 years
        
        if not telefone.isdecimal():
            raise ValidationError(detail="Informe um telefone válido.")
        if nascimento >= time:
            raise ValidationError(detail="Você precisa ter mais que 16 anos.")