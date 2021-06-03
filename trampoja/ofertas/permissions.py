from rest_framework import permissions


class IsOwnerOrReadOnly():

    def has_object_permission(request, oferta):
        if request.method in permissions.SAFE_METHODS:
            return True
        if oferta.owner == request.user:
            return True
        return False
