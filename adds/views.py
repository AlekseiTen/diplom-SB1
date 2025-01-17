from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from adds.filters import AdsFilter
from adds.models import Ad, Comment
from adds.permissions import IsAdminOrOwnerOrReadOnly
from adds.serializers import AdSerializer, CommentSerializer


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrOwnerOrReadOnly,
    ]
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = AdsFilter  # Поиск по названию

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )  # Установить текущего пользователя как автора


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        # Извлекаем ID объявления из URL (используем параметр ad_id)
        ad_id = self.kwargs["ad_id"]
        ad = Ad.objects.get(id=ad_id)
        serializer.save(
            author=self.request.user, ad=ad
        )  # Привязываем комментарий к объявлению
