# Generated by Django 5.0.1 on 2024-01-10 10:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0003_alter_categories_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('price', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to='images')),
                ('description', models.CharField(max_length=100)),
                ('quantity', models.PositiveIntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommapp.categories')),
            ],
        ),
    ]
