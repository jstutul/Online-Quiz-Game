# Generated by Django 3.2 on 2021-06-12 19:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App_Quiz', '0005_categoty_attemp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoty',
            name='attemp',
        ),
        migrations.AddField(
            model_name='categoty',
            name='attemp1',
            field=models.ManyToManyField(blank=True, null=True, related_name='attemp1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='categoty',
            name='attemp2',
            field=models.ManyToManyField(blank=True, null=True, related_name='attemp2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='categoty',
            name='attemp3',
            field=models.ManyToManyField(blank=True, null=True, related_name='attemp3', to=settings.AUTH_USER_MODEL),
        ),
    ]
