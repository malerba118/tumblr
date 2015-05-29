# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0002_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('activity_type', models.SmallIntegerField(choices=[(0, 'Post'), (1, 'Reblog'), (2, 'Like'), (3, 'Comment'), (4, 'Follow')])),
                ('object_fk', models.IntegerField()),
                ('subject', models.ForeignKey(to='blogging.Blog')),
            ],
        ),
    ]
