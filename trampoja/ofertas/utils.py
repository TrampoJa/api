from django.http import *
import datetime
from django.utils import timezone

class Utils:

    def validator(data):
        valor = data['valor']
        data = data['date_inicial']   
        
        if valor < 10:
            raise Http404
        elif data < datetime.date.today():
            raise Http404