# Generated by Django 4.1.2 on 2022-10-16 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_alter_class_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='post_survey_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='test',
            name='pre_survey_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='class',
            name='semester',
            field=models.IntegerField(choices=[(0, 'Fall'), (1, 'Spring')], default=0, max_length=100),
        ),
    ]