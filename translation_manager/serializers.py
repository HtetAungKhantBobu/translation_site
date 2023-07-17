from rest_framework import serializers

from translation_manager.models import Chapter, Translation


class ConciseTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class ConciseChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = [
            field.name
            for field in Chapter._meta.fields
            if field.name not in ["contents"]
        ]
        read_only_fields = ("id",)
        optional_fields = [field for field in fields if field != "id"]


class DetailedTranslationSerializer(ConciseTranslationSerializer):
    title = serializers.CharField(required=False)
    chapters = ConciseChapterSerializer(source="chapter_set", many=True, read_only=True)

    class Meta:
        model = Translation
        fields = (
            ["title"]
            + [
                field.name
                for field in Translation._meta.fields
                if field.name not in ["title"]
            ]
            + ["chapters"]
        )
        read_only_fields = ("id",)
        optional_fields = [field for field in fields if field != "id"]


class DetailedChapterSerializer(ConciseChapterSerializer):
    title = serializers.CharField(required=False)
    published_date = serializers.DateTimeField(required=False, read_only=True)
    parent_translation = serializers.IntegerField(
        required=False, source="parent_translation.id"
    )

    class Meta:
        model = Chapter
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
        optional_fields = [field for field in fields if field != "id"]

    def create(self, validated_data):
        parent_translation = Translation.objects.get(
            id=validated_data["parent_translation"]["id"]
        )
        validated_data["parent_translation"] = parent_translation
        return Chapter.objects.create(**validated_data)
