from rest_framework import serializers
from translation_manager.models import Translation, Chapter


class ConciseTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = "__all__"


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = "__all__"


class DetailedTranslationSerializer(ConciseTranslationSerializer):
    chapters = ChapterSerializer(source="chapter_set", many=True, read_only=True)

    class Meta:
        model = Translation
        fields = [field.name for field in Translation._meta.fields] + ["chapters"]
