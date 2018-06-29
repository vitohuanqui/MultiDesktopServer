from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from rest_framework import mixins, permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from accounts.models import Document, Log
from accounts.serializers import DocumentSerializer, UserSerializer, \
    UserLeapSerializer, UserDocumentShareSerializer, UpdateDocumentSerializer


class ShareListDocumentViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (IsAuthenticated,)

    def filter_queryset(self, queryset):
        return [log.document for log in self.request.user.log_set.filter(is_sending=True)]


class ShareDocumentViewSet(GenericViewSet, mixins.UpdateModelMixin):
    queryset = Document.objects.all()
    serializer_class = UserDocumentShareSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        for user in User.objects.all().exclude(id=instance.user.id):
            log, created = Log.objects.get_or_create(user=user, document=instance)
            log.is_sending = True
            log.save()
        return Response(serializer.data)


class DocumentViewSet(GenericViewSet, mixins.CreateModelMixin,
                      mixins.ListModelMixin, mixins.DestroyModelMixin):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (IsAuthenticated,)

    def filter_queryset(self, queryset):
        qs = super(DocumentViewSet, self).filter_queryset(queryset)
        return qs.filter(user=self.request.user)


class UpdateDocumentView(GenericViewSet, mixins.UpdateModelMixin):

    queryset = Document.objects.all()
    serializer_class = UpdateDocumentSerializer
    permission_classes = (IsAuthenticated,)


class CreateUserView(GenericViewSet, mixins.UpdateModelMixin):

    queryset = User.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        obj = get_object_or_404(queryset, username=self.request.data['username'])

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CreateLeapUserView(GenericViewSet, mixins.CreateModelMixin):

    queryset = User.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserLeapSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
