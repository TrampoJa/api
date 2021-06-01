from rest_framework.exceptions import ValidationError


class Utils:

    def validator(data):
        telefone = data['telefone']
        cnpj = data['cnpj']

        if not telefone.isdecimal():
            raise ValidationError(detail="Informe um telefone válido.")
        if not cnpj.isdecimal():
            raise ValidationError(detail="Informe um cpf ou cnpj válido.")
