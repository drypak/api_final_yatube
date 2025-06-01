from posts.models import Comment, Follow, Group, Post, User
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


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

    Автор - readonly и по слагу.
    Пост - readonly и по pk.
    """

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


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

    Пользователь (user) - readonly, подписка (following) - по слагу.
    Валидация - запрещена подписка на самого себя и дубли.
    """

    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def get_current_user(self):
        """Возвращает юзера из контекста запроса."""
        return self.context['request'].user

    def validate(self, data):
        """Валидация: запрещена подписка на самого себя и дубли."""
        user = self.get_current_user()
        following = data['following']
        if user == following:
            raise serializers.ValidationError
        if Follow.objects.filter(
            user=user,
            following=following
        ).exists():
            raise serializers.ValidationError
        return data

    def create(self, validated_data):
        """Добавляет текущего юзера в validated_data при создании подписки."""
        user = self.get_current_user()
        validated_data['user'] = user
        return super().create(validated_data)
