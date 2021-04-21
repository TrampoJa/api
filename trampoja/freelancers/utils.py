from django.http import *
import datetime
from django.utils import timezone

class Utils:

    def validator(data):
        telefone = data['telefone']
        nascimento = data['nascimento']
        time = datetime.date.today() + datetime.timedelta(weeks=-834) # 16 years
        
        if not telefone.isdecimal():
            raise Http404
        if nascimento >= time:
            raise Http404