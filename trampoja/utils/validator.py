from rest_framework.exceptions import ValidationError
from re import search


class Validator:

    def __init__(self, data):
        for field in data:
            try:
                method = getattr(self, field)
                method(data[field])
            except AttributeError:
                ...

    # users
    def password(self, password):
        passLen = len(password)
        if (passLen < 6 or passLen > 30):
            raise ValidationError(detail='Senha inválida.')

    def email(self, email):
        regex = r'^[\w_.+-]+@[\w-]+\.[\w.-]+$'
        if not search(regex, email):
            raise ValidationError(detail='Email inválido.')

    def first_name(self, first_name):
        regex = r"[^A-Za-zÀ-Ÿà-ÿ\s']"
        if search(regex, first_name):
            raise ValidationError(detail='Primeiro nome inválido.')

    def last_name(self, last_name):
        regex = r"[^A-Za-zÀ-Ÿà-ÿ\s']"
        if search(regex, last_name):
            raise ValidationError(detail='Ultimo nome inválido.')

    # ofertas
    def valor(self, valor):
        if (valor < 10):
            raise ValidationError(detail='O valor mínimo é 10 reais por hora')

    def date_inicial(self, date_inicial):
        from datetime import date
        if (date_inicial < date.today()):
            raise ValidationError(detail='Esta data já passou')

    # freelancers
    def telefone(self, telefone):
        regex = r'[^\d]'
        if search(regex, telefone):
            raise ValidationError(detail='Informe um telefone válido.')

        lenght = len(telefone)
        if (lenght < 10 or lenght > 11):
            raise ValidationError(detail='Informe um telefone válido.')

    def rg(self, rg):
        regex = r'[^\d]'
        if search(regex, rg):
            raise ValidationError(detail='Informe um rg válido.')

    def nascimento(self, nascimento):
        from datetime import date, timedelta
        time = date.today() + timedelta(weeks=-834)  # 16 years
        if (nascimento >= time):
            raise ValidationError(detail='Você precisa ter mais que 16 anos.')

    def foto(self, foto):
        import imghdr

        if not foto:
            raise ValidationError(detail='Foto inválida')

        permitidas = ['png', 'jpg', 'jpeg']
        if imghdr.what(foto) not in permitidas:
            raise ValidationError(detail='Foto inválida')

    # estabelecimentos
    def cnpj(self, cnpj):
        regex = r'[^\d]'
        if search(regex, cnpj):
            raise ValidationError(detail='Informe um cnpj válido.')

        if (len(cnpj) != 14):
            raise ValidationError(detail='Informe um cnpj válido.')

    def nome(self, nome):
        regex = r'[^\w\s]u'
        if search(regex, nome):
            raise ValidationError(detail='Informe um nome válido.')

    def razao_social(self, razao_social):
        regex = r'[^\w\s]'
        if search(regex, razao_social):
            raise ValidationError(detail='Informe uma razão social válida.')

    def logo(self, logo):
        import imghdr

        if not logo:
            raise ValidationError(detail='Logo inválida')

        permitidas = ['png', 'jpg', 'jpeg']
        if imghdr.what(logo) not in permitidas:
            raise ValidationError(detail='Logo inválida')
