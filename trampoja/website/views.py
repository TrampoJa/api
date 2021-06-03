# @author Luiz Roberto Dendena luiz.dendena@gmail.com

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


class Index():

    @api_view(['GET'])
    def get(request, format=None):
        return Response({"Tudo certo por aqui": ":)"},
                        status=status.HTTP_200_OK)
