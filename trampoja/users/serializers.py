from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()

    def get_group(self, user):
        try:
            return user.groups.get().name
        except Exception:
            return

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'telefone',
            'group',
        ]
