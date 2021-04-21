class IsFreelancerOrReadOnly():
    
    def has_object_permission(request):
        if request.user.last_name == "Freelancer":
            return True
        return False