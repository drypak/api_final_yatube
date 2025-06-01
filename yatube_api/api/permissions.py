from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Чтение для всех, создание только для аутентифицированных."""

    def has_permission(self, request, view):
        """
        Разрешить доступ, если:.

        - метод безопасный, например GET
        - пользователь авторизован
        """
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Аналогично has_permission.

        но проверяем, что юзер - автор объекта.
        """
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
