import base64

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings

from accounts.models import Document, UserIP


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_representation(self, value):
        if not value:
            return None

        use_url = getattr(self, 'use_url', api_settings.UPLOADED_FILES_USE_URL)

        if use_url:
            if not getattr(value, 'url', None):
                # If the file has not been saved it may not have a URL.
                return None
            url = settings.BASE_DIR + '/../' + value.url
            with open(url, 'rb') as f:
                return base64.b64encode(f.read())
        return value.name

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class DocumentSerializer(serializers.ModelSerializer):

    file_b64 = Base64ImageField(source='file')

    class Meta:
        model = Document
        fields = ('id', 'shared', 'file_b64', 'x', 'y', 'z')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(DocumentSerializer, self).create(validated_data)


class UserSerializer(serializers.ModelSerializer):

    #password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()
    token_id = serializers.CharField(required=False)

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)

        return token.key

    def create(self, validated_data):
        print("asdads")
        user, created = get_user_model().objects.get_or_create(
            username=validated_data['username']
        )
        if created:
            user.set_password(validated_data['username'])
            user.save()
        token = Token.objects.create(user=user, key=validated_data['token_id'])
        
        return user

    def update(self, instance, validated_data):
        print(validated_data)
        user, created = get_user_model().objects.get_or_create(
            username=validated_data['username']
        )
        print(created)
        if created:
            print("CREO")

            user.set_password(validated_data['username'])
            user.save()
            token = Token.objects.create(user=user, key=validated_data['token_id'])
        else:
            print("actualiza")
            Token.objects.filter(user=user).delete()
            Token.objects.create(user=user, key=validated_data['token_id'])

        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'token', 'token_id')


class UserLeapSerializer(serializers.ModelSerializer):

    ip = serializers.CharField(source='userip.ip')

    def create(self, validated_data):
        user, created = get_user_model().objects.get_or_create(
            username=validated_data['username']
        )
        if created:
            user.set_password(validated_data['username'])
            user.save()
            ip = UserIP.objects.create(user=user, ip=validated_data['userip']['ip'])
        else:
            user.userip.ip = validated_data['userip']['ip']
            user.userip.save()

        return user

    def get_ip(self, obj):

        return obj.userip.ip

    class Meta:
        model = get_user_model()
        fields = ('username', 'ip')


class UserDocumentShareSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ('shared', )


class UpdateDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ('x', 'y', 'z')
