class BaseEmailMessage():
    def __init__(self, email=None, nome=None, oferta=None):
        self.email = email
        self.oferta = oferta
        self.nome = nome
        self.from_email = "testesmtp@trampoja.com"
        self.titulo = "TrampoJá"


class BaseWhatsAppMessage():
    def __init__(self, number=None, nome=None, oferta=None):
        self.number = number
        self.nome = nome
        self.oferta = oferta
        self.token = "87xckk7h57zngqcu1qp0sleuf8982o"
        self.url = "https://v4.chatpro.com.br/chatpro-hlx44myihd/api/v1/send_message"
        self.headers = {
            'Authorization': self.token,
            'cache-control': "no-cache"
        }
