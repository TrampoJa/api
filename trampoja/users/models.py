from django.contrib.auth.models import Group


class User:

    def set_group(user, groupName):
        group = Group.objects.get_by_natural_key(groupName)
        user.groups.set([group])
        user.save()
        return user