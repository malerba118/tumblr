# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('blogging', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('activity_type', models.SmallIntegerField(choices=[(0, 'Post'), (1, 'Reblog'), (2, 'Like'), (3, 'Comment'), (4, 'Follow')])),
                ('object_fk', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
                ('subject', models.ForeignKey(to='blogging.Blog')),
            ],
        ),
    ]
