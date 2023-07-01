from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from translation_site.permissions import *
from user_manager.serializers import LoginSerializer


class AuthViewSet(viewsets.GenericViewSet):
    permission_class = (AllowAny,)

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_class if self.serializer_class else BaseSerializer

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=LoginSerializer,
    )
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


# Create your views here.
