# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('score', models.IntegerField(verbose_name='Score')),
                ('comment', models.CharField(max_length=400, verbose_name='Comment')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('published', models.BooleanField(default=True)),
                ('content_type', models.ForeignKey(related_name='comments', to='contenttypes.ContentType')),
                ('user', models.ForeignKey(related_name='_', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
