from rest_framework import viewsets
from core.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Viewset to Create, List, Retrieve, Delete User"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


    # def get_queryset(self):
    #     username = self.request.query_params.get('username', None)
    #     queryset = User.objects.all()

    #     if username:
    #         queryset = queryset.filter(username=username)
    #     return queryset