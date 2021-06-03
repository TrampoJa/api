from datetime import date

from rest_framework.exceptions import ValidationError


class Utils:

    def validator(data):
        valor = data['valor']
        if valor < 10:
            raise ValidationError(detail="O valor mínimo é 10 reais por hora")

        data = data['date_inicial']
        if data < date.today():
            raise ValidationError(detail="Esta data já passou")
