from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .permissions import IsAdmin
from .serializers import User, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('id')
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated], name='user_me')
    def me(self, request, version, pk=None):
        serializer = UserSerializer(instance=request.user)

        if request.method == 'PATCH':
            serializer = UserSerializer(
                instance=request.user, data=request.data, partial=True,
            )
            serializer.fields['role'].read_only = True
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
