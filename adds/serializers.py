from rest_framework import serializers

from adds.models import Ad, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.email")  # Только для чтения

    class Meta:
        model = Comment
        fields = ["id", "text", "author", "created_at", "updated_at",]


class AdSerializer(serializers.ModelSerializer):
    # выводит email автора, но не дает его изменить.
    author = serializers.ReadOnlyField(source="author.email")

    # для отображения списка комментов связанных с объявлением
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Ad
        fields = [
            "id",
            "title",
            "price",
            "description",
            "author",
            "created_at",
            "updated_at",
            "comments",
        ]
