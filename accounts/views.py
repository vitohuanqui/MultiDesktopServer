from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import mixins, permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from accounts.models import Document
from accounts.serializers import DocumentSerializer, UserSerializer


class DocumentViewSet(GenericViewSet, mixins.CreateModelMixin,
                      mixins.ListModelMixin):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (IsAuthenticated,)

    def filter_queryset(self, queryset):
        qs = super(DocumentViewSet, self).filter_queryset(queryset)
        return qs.filter(user=self.request.user)


class CreateUserView(GenericViewSet, mixins.CreateModelMixin):

    queryset = User.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
