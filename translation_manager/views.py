from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from translation_manager.models import Chapter, Translation
from translation_manager.serializers import (
    ConciseChapterSerializer,
    ConciseTranslationSerializer,
    DetailedChapterSerializer,
    DetailedTranslationSerializer,
)
from translation_site.permissions import *
from translation_site import params


class TranslationViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = Translation.objects.all().order_by("title")
    serializer_class = ConciseTranslationSerializer

    def get_serializer_class(self):
        if self.serializer_class is None:
            return BaseSerializer
        return self.serializer_class

    @swagger_auto_schema(
        manual_parameters=[
            params.Q,
            params.ASC,
        ],
    )
    def list(self, request, *args, **kwargs):
        """
        List all the translations/series sorted by title in ascending order
        params:
            - q = optional Search
            - asc = optional order (default ascending)
        """
        data = self.queryset
        q = request.query_params.get("q")
        asc = request.query_params.get("asc")
        if q:
            data = data.filter(title__icontains=q.lower())
        if asc and asc.lower() == "false":
            data = data.order_by("-title")

        serializer = self.get_serializer(data, many=True)
        return Response(
            data={"all_translations": serializer.data},
            status=status.HTTP_200_OK,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @swagger_auto_schema(methods=["GET", "PATCH"])
    @action(
        methods=["GET", "PATCH"],
        permission_classes=[AllowAny],
        detail=True,
        serializer_class=DetailedTranslationSerializer,
    )
    def details(self, request, pk):
        """
        A detailed view for each chapter
        """
        if request.method == "GET":
            translation = get_object_or_404(Translation, id=pk)
            return Response(
                self.get_serializer(translation).data,
                status=status.HTTP_200_OK,
            )
        elif request.method == "PATCH":
            translation = get_object_or_404(Translation, id=pk)
            serializer = self.get_serializer(translation, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )


class ChapterViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = Chapter.objects.all().order_by("created_at")
    serializer_class = ConciseChapterSerializer

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
            data={"all_chapters": serializer.data},
            status=status.HTTP_200_OK,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @swagger_auto_schema(method="GET")
    @action(
        methods=["GET", "PATCH"],
        permission_classes=[IsTranslatorOrReadOnly],
        detail=True,
        serializer_class=DetailedChapterSerializer,
    )
    def details(self, request, pk):
        """
        A detailed view for each chapter
        """
        if request.method == "GET":
            chapter = get_object_or_404(Chapter, id=pk)
            return Response(
                self.get_serializer(chapter).data,
                status=status.HTTP_200_OK,
            )
        elif request.method == "PATCH":
            chapter = get_object_or_404(Chapter, id=pk)
            serializer = self.get_serializer(chapter, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )


# Create your views here.
