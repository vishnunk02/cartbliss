# Generated by Django 5.0.1 on 2024-01-17 10:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0008_placeorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='placeorder',
            name='cart',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='ecommapp.carts'),
            preserve_default=False,
        ),
    ]