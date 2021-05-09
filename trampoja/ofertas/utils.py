import datetime

from django.http import *
from django.utils import timezone

from rest_framework.exceptions import ValidationError


class Utils:

    def validator(data):
        valor = data['valor']
        data = data['date_inicial']   
        
        if valor < 10:
            raise ValidationError(detail="O valor mínimo é 10 reais por hora")
        elif data < datetime.date.today():
            raise ValidationError(detail="Esta data já passou")