from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Group, Post
from .mixins import ListCreateViewSet
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CommentSerializer,
    GroupSerializer,
    FollowSerializer,
    PostSerializer,
)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Просто смотрим группы.

    Только для чтения, без создания и обновления.
    Доступ: всем, но гостям только чтение.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class PostViewSet(viewsets.ModelViewSet):
    """
    Создание, чтение, обновление, удаление постов.

    править и удалять можно только свои посты.
    Пагинация включена.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Когда создается пост, автором становится текущий юзер."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Комменты к постам.

    Все комменты к посту можно посмотреть,
    но создание комментов только авторизованным.
    менять и удалять может только автор.
    """

    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_post(self):
        """Находим пост из урла."""
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        """Получаем все комменты к посту."""
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """При случае создания коммента сохраним автора и пост."""
        serializer.save(
            author=self.request.user,
            post=self.get_post()
        )


class FollowViewSet(ListCreateViewSet):
    """
    Подписки.

    Можно посмотреть на кого подписан текущий юзер.
    И подписаться на нового.
    Поиск по никнейму.
    """

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Получаем все подписки текущего юзера."""
        return self.request.user.follows.all()

    def perform_create(self, serializer):
        """При создании подписки ставим текущего юзера."""
        serializer.save(user=self.request.user)
