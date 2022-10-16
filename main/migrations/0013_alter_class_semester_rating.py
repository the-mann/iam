# Generated by Django 4.1.2 on 2022-10-15 16:42

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0012_class_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='semester',
            field=models.CharField(default='Fall', max_length=100, verbose_name=main.models.SEMESTER_CHOICE),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confidence', models.IntegerField(choices=[(0, 'Bad'), (1, 'Meh'), (2, 'Good')])),
                ('date_rated', models.DateTimeField(verbose_name=datetime.datetime.now)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.test')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moods', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
