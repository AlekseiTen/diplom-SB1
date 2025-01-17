from django.urls import path, include
from rest_framework.routers import DefaultRouter

from adds.views import AdViewSet, CommentViewSet

router = DefaultRouter()
router.register("ads", AdViewSet, basename="ads")

# Для добавления комментариев к объявлению используем URL вида /ads/{ad_id}/comments/
router.register(r"ads/(?P<ad_id>\d+)/comments", CommentViewSet, basename="comments")

urlpatterns = [
    path("", include(router.urls)),
]
