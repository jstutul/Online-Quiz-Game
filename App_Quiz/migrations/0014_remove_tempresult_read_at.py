# Generated by Django 3.2 on 2021-06-14 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Quiz', '0013_tempresult_read_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tempresult',
            name='read_at',
        ),
    ]
