# Generated by Django 4.1.2 on 2022-10-16 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_alter_class_semester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='semester',
            field=models.IntegerField(default=0, max_length=100, verbose_name=[(0, 'Fall'), (1, 'Spring')]),
        ),
    ]
