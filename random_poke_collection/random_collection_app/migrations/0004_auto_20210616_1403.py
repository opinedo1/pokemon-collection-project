# Generated by Django 2.2 on 2021-06-16 21:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('random_collection_app', '0003_post_posted_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to='random_collection_app.Post'),
        ),
    ]
