class IsEstabelecimentoOrReadOnly():

    def has_object_permission(request):
        if request.user.groups.get().name == "Estabelecimento":
            return True
        return False
