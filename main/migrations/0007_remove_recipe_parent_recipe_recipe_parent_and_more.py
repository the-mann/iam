# Generated by Django 4.0.3 on 2022-04-10 18:51

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_recipe_favorites_alter_recipe_edited_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='parent_recipe',
        ),
        migrations.AddField(
            model_name='recipe',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='main.recipe'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='edited_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 10, 13, 51, 7, 743378)),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='favorites',
            field=models.ManyToManyField(related_name='favorites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='posted_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 10, 13, 51, 7, 743363)),
        ),
    ]
