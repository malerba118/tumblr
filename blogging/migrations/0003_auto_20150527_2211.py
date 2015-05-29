# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0002_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='root',
            field=models.ForeignKey(to='blogging.Post', null=True),
        ),
    ]
