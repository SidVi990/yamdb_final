from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Category


class TitleInputSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        default=GenreSerializer(required=True)
    )
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        default=CategorySerializer(required=True)
    )

    def validate_year(self, value):
        if value > timezone.now().year:
            raise ValidationError('You cannot take title from future!')
        return value

    class Meta:
        fields = '__all__'
        model = Title


class TitleResultSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('author', 'title')

    def validate(self, data):
        if self.context['request'].method == "POST" and Review.objects.filter(
                author=self.context['request'].user,
                title_id=self.context['title_id']
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    review = SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'review')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def is_valid(self, raise_exception=False):
        assert hasattr(self, 'initial_data'), (
            'Cannot call .is_valid() as no data= keyword argument was '
            'passed when instantiating the serializer instance.'
        )
        if ('username' in self.initial_data.keys()
                and 'email' in self.initial_data.keys()):
            if User.objects.filter(
                    username=self.initial_data['username'],
                    email=self.initial_data['email']
            ).exists():
                self._validated_data = self.initial_data
                return True
        if not hasattr(self, '_validated_data'):
            try:
                self._validated_data = self.run_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = {}
                self._errors = exc.detail
            else:
                self._errors = {}

        if self._errors and raise_exception:
            raise ValidationError(self.errors)

        return not bool(self._errors)

    def validate_username(self, value):
        if str.lower(value) in ('me'):
            raise ValidationError('Не корректное имя пользователя')
        return value

    def validate(self, data):
        if User.objects.filter(username=data['username'], email=data['email']):
            pass
        return data


class RecieveTokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
