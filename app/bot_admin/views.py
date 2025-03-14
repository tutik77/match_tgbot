from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import User, UserQuery
from .serializers import UserSerializer, UserQuerySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, user_id=pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    def search(self, request):
        keywords_list = request.data.get('keywords', [])

        query = Q()
        for keyword in keywords_list:
            query |= Q(description_keywords__icontains=keyword.strip())

        users = User.objects.filter(query).distinct()[:7]

        if not users.exists():
            return Response({"message": "No users found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)


class UserQueryViewSet(viewsets.ModelViewSet):
    queryset = UserQuery.objects.all()
    serializer_class = UserQuerySerializer  

