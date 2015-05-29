# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('newsfeed', '0002_auto_20150527_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='object_fk',
            field=models.PositiveIntegerField(),
        ),
    ]
