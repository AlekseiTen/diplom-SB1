from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrOwnerOrReadOnly(BasePermission):
    """
    Разрешает редактировать и удалять объявление только:
    - Администраторам (могут редактировать/удалять любое объявление).
    - Владельцам (могут редактировать/удалять только свои объявления).
    Просмотр доступен всем.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:  # Безопасные методы (GET, HEAD, OPTIONS)
            return True

        # Администратор имеет доступ ко всем операциям
        if request.user.role == "admin":
            return True

        return obj.author == request.user  # Проверка на автора
