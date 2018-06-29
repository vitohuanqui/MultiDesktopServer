from django.contrib.auth.models import User
from django.db import models


class Document(models.Model):
    file = models.ImageField('archivo', upload_to='documentos/')
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='user')
    shared = models.BooleanField(default=False)


class UserIP(models.Model):
    ip = models.CharField('ip', max_length=32)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='user')


class Log(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='user')
    is_sending = models.BooleanField(default=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True)
#