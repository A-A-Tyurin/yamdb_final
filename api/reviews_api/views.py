from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilter
from .mixins import ListModelViewSet
from .permissions import AdminOrReadOnly, MainPermission
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReadTitleSerializer,
                          ReviewSerializer, WriteTitleSerializer)


class CategoryViewSet(ListModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListModelViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)
    http_method_names = ['get', 'post', 'delete']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg(
        'reviews__score')
    ).order_by('-id')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ReadTitleSerializer
        return WriteTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (MainPermission, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(title=get_object_or_404(Title,
                        pk=self.kwargs.get('title_id')),
                        author=self.request.user)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (MainPermission, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(review=get_object_or_404(Review,
                        pk=self.kwargs.get('review_id')),
                        author=self.request.user)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()
