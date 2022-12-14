# Generated by Django 4.1.2 on 2022-10-16 13:44

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_send_alter_class_semester'),
    ]

    operations = [
        migrations.RenameField(
            model_name='class',
            old_name='class_name',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='class',
            name='meeting_time',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='class',
            name='semester',
            field=models.CharField(default='Fall', max_length=100, verbose_name=main.models.SEMESTER_CHOICE),
        ),
    ]
