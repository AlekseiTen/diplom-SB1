from rest_framework.permissions import BasePermission


class IsAdminOrOwnerOrReadOnly(BasePermission):
    """
    Разрешает редактировать и удалять объявление только:
    - Администраторам (могут редактировать/удалять любое объявление).
    - Владельцам (могут редактировать/удалять только свои объявления).
    """

    def has_object_permission(self, request, view, obj):

        # Администратор имеет доступ ко всем операциям
        if request.user.role == "admin":
            return True

        return obj.author == request.user  # Проверка на автора
