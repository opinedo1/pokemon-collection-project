# Generated by Django 2.2 on 2021-06-17 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('random_collection_app', '0005_auto_20210616_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='src',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]