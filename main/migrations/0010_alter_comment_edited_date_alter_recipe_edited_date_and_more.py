# Generated by Django 4.0.3 on 2022-04-12 16:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_rename_recipes_comment_recipe_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='edited_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='edited_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 12, 11, 4, 42, 493783)),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='posted_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 12, 11, 4, 42, 493771)),
        ),
    ]