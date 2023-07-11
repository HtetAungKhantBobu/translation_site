from django.db import models
from user_manager.models import User


class Genre(models.Model):
    name = models.CharField("name of the genre", max_length=255, unique=True)
    description = models.TextField("description of the genre")

    def __str__(self) -> str:
        return self.name


class Translation(models.Model):
    class Type(models.TextChoices):
        WEB_NOVEL = "WN"
        LIGHT_NOVEL = "LN"

    class Language(models.TextChoices):
        ENGLISH = "EN"
        JAPANESE = "JP"
        CHINESE = "CN"
        KOREAN = "KR"

    class Status(models.TextChoices):
        ON_GOING = "ON"
        HIATUS = "HI"
        ENDED = "ED"
        UNKNOWN = "UK"

    title = models.CharField("Title or Name of the translation.", max_length=255)
    author = models.CharField(
        "Author(s) of the source material", max_length=255, blank=True
    )
    source_language = models.CharField(
        "Language of the main source.",
        max_length=2,
        choices=Language.choices,
        default=Language.JAPANESE,
    )
    genres = models.ManyToManyField(Genre, blank=True)
    synopis = models.TextField("Synopis of the series.", blank=True)
    type = models.CharField(
        "Type of the source material.",
        max_length=2,
        choices=Type.choices,
        default=Type.WEB_NOVEL,
    )
    status = models.CharField(
        "Current Status of the translation.",
        max_length=2,
        choices=Status.choices,
        default=Status.UNKNOWN,
    )

    class Meta:
        indexes = [
            models.Index(fields=["title"], name="translation_title_idx"),
        ]

    def __str__(self):
        return self.title


class Chapter(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = "PB"
        IN_PROGRESS = "IP"
        UNKNOWN = "UK"

    title = models.CharField("Chapter Title", max_length=255)
    serial = models.IntegerField("Chapter No.", default=0)
    parent_translation = models.ForeignKey(
        Translation,
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        "Current translation status of the chapter",
        max_length=2,
        choices=Status.choices,
        default=Status.UNKNOWN,
    )
    contents = models.TextField("Translated Content", blank=True)
    published_date = models.DateTimeField(
        "Published Date and Time", blank=True, null=True
    )
    translator = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["serial"], name="chapter_no_idx"),
            models.Index(
                fields=["parent_translation"], name="chapter_parent_translation_idx"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.parent_translation} | Chapter {self.serial}"
