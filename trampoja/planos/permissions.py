class IsEstabelecimentoOrReadOnly():

    def has_object_permission(request):
        if request.user.last_name == "Estabelecimento":
            return True
        return False