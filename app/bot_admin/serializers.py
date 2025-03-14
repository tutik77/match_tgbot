from rest_framework import serializers
from .models import User, UserQuery

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuery
        fields = '__all__'