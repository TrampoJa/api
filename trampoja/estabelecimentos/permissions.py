from rest_framework import permissions

class IsOwnerOrReadOnly():

    def has_object_permission(request, estabelecimento):
        if request.method in permissions.SAFE_METHODS:
            return True
        if estabelecimento.owner == request.user:
            return True
        return False