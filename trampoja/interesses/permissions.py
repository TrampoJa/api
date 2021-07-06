class IsFreelancerOrReadOnly():

    def has_object_permission(request):
        if request.user.groups.get().name == "Freelancer":
            return True
        return False
