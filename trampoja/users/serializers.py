from rest_framework import serializers
from users.models import User
from ofertas.models import Ofertas

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name'
        ]