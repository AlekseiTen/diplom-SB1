import django_filters

from .models import Ad


class AdsFilter(django_filters.FilterSet):
    """
    Фильтр для модели объявления
    """

    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Ad
        fields = ["title"]
