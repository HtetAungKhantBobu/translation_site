from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from translation_manager.models import Translation, Chapter
from translation_site.permissions import *
from translation_manager.serializers import (
    ConciseTranslationSerializer,
    ChapterSerializer,
    DetailedTranslationSerializer,
)


class TranslationViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = Translation.objects.all()
    serializer_class = ConciseTranslationSerializer

    def get_serializer_class(self):
        if self.serializer_class is None:
            return BaseSerializer
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        """
        List all the translations/series
        """
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(
            data={"all_translations": serializer.data},
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(method="GET")
    @action(
        methods=["GET"],
        permission_classes=[AllowAny],
        detail=True,
        serializer_class=DetailedTranslationSerializer,
    )
    def details(self, request, pk):
        """
        A detailed view for each chapter
        """
        translation = get_object_or_404(Translation, id=pk)
        return Response(
            self.get_serializer(translation).data,
            status=status.HTTP_200_OK,
        )


class ChapterViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    def get_serializer_class(self):
        if self.serializer_class is None:
            return BaseSerializer
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        """
        List all the Chapters
        """
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(
            data={"all_translations": serializer.data},
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(method="GET")
    @action(
        methods=["GET"],
        permission_classes=[AllowAny],
        detail=True,
        serializer_class=ChapterSerializer,
    )
    def details(self, request, pk):
        """
        A detailed view for each chapter
        """
        chapter = get_object_or_404(Chapter, id=pk)
        return Response(
            self.get_serializer(chapter).data,
            status=status.HTTP_200_OK,
        )


# Create your views here.
