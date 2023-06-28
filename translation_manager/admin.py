from django.contrib import admin
from django.contrib.admin import TabularInline
from translation_manager.models import Translation, Chapter, Genre


class ChapterInline(TabularInline):
    model = Chapter
    fields = ["id", "serial", "title", "published_date", "status"]
    ordering = ("created_at",)
    classes = ("collapse",)
    extra = 1


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ["title", "source_language", "type", "status"]
    list_filter = ["source_language", "type", "status"]
    search_fields = ["title"]
    filter_horizontal = ("genres",)
    inlines = (ChapterInline,)


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ["parent_translation", "serial", "status", "published_date"]
    list_filter = ["status", "parent_translation__title"]
    search_fields = ["parent_translation__title", "title"]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
