# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsfeed', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='subject',
        ),
        migrations.DeleteModel(
            name='Activity',
        ),
    ]
