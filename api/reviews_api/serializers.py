from django.utils import timezone
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id']
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id']
        model = Category


class ReadTitleSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    genre = GenreSerializer(many=True, read_only=True,)
    rating = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year = timezone.now().year
        if (value > year):
            raise serializers.ValidationError('Будущее запрещено!')
        return value


class WriteTitleSerializer(ReadTitleSerializer):
    description = serializers.CharField(required=False)
    category = serializers.SlugRelatedField(many=False, slug_field='slug',
                                            read_only=False,
                                            queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(many=True, slug_field='slug',
                                         read_only=False,
                                         queryset=Genre.objects.all())
    rating = serializers.IntegerField(required=False, read_only=False)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(many=False,
                                          slug_field='username',
                                          read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(many=False,
                                          slug_field='username',
                                          read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        review = Review.objects.filter(
            title=self.context['view'].kwargs.get('title_id'),
            author=self.context['request'].user
        )
        if review.exists() and self.context['request'].method == 'POST':
            raise serializers.ValidationError('Только одно ревью!')
        return data
