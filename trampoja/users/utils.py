import re
from django.http import *

class Utils:

    def password_validator(self, password):
        if len(password) < 6:
            raise Http404

    def email_validator(self, email):
        regex_com = '^[a-z0-9]+[\._]?[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        regex_com_br = '^[a-z0-9]+[\._]?[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}\w+[.]\w{2,3}$'
        if re.search(regex_com, email) or re.search(regex_com_br, email):
            pass
        else:    
            raise Http404

    def validator(self, email, password):
        self.password_validator(password)
        self.email_validator(email)