# Generated by Django 4.1.2 on 2022-10-16 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_delete_send_alter_class_professor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='date',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='test',
            name='starts_at',
            field=models.TimeField(),
        ),
    ]
