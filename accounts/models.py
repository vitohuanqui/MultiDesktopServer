from django.contrib.auth.models import User
from django.db import models


class Document(models.Model):
    file = models.ImageField('archivo', upload_to='documentos/')
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='user')
