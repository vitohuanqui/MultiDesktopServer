# Generated by Django 2.0.5 on 2018-06-11 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='x',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='y',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='z',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]