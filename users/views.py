from rest_framework import viewsets
from core.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Viewset to Create, List, Retrieve, Delete User"""
    queryset = User.objects.all()
    serializer_class = UserSerializer