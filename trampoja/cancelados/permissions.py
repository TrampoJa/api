from estabelecimentos.models import Estabelecimentos
from freelancers.models import FreeLancers

class IsOwnerOrReadOnly():

    def has_object_permission(request):
        try:
            freelancer = FreeLancers.objects.get(owner=request.user)
            if isinstance(freelancer, FreeLancers):
                if request.user == freelancer.owner:
                    return True
        except Exception:
            pass

        try:
            estabelecimento = Estabelecimentos.manager.get(owner=request.user)
            if isinstance(estabelecimento, Estabelecimentos):
                if request.user == estabelecimento.owner:
                    return True
        except Exception:
            pass
        
        return False