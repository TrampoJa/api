from rest_framework import permissions

class IsOwnerOrReadOnly():

    def has_object_permission(request, freelancer):
        if request.method in permissions.SAFE_METHODS:
            return True
        if freelancer.owner == request.user:
            return True
        return False