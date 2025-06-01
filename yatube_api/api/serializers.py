from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from constants import (
    FOLLOW_FIELDS,
    VALIDATOR_MESSAGE,
    FOLLOW_SELF_MESSAGE
)

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Post.

    Автор выводится по слагу и только для чтения.
    """

    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.

    author отображается по слагу, для чтения.
    post - только для чтения.
    """

    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Group.

    Поля: все.
    """

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Follow.

    Пользователь (user) - по слагу,
    подставляется из текущего запроса CurrentUserDefault.
    Подписка (following) - по слагу, обязательна.
    Валидация: подписка на самого себя запрещена.
    """

    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = FOLLOW_FIELDS
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=FOLLOW_FIELDS,
                message=VALIDATOR_MESSAGE
            )
        ]

    def validate(self, data):
        """Подписка на самого себя запрещена."""
        user = data.get('user')
        following = data.get('following')
        if user == following:
            raise serializers.ValidationError(
                {'following': FOLLOW_SELF_MESSAGE}
            )
        return data
