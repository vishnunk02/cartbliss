# Generated by Django 5.0.1 on 2024-02-15 05:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0011_addressmodel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AddressModel',
            new_name='Address',
        ),
    ]
