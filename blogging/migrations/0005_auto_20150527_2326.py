# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0004_auto_20150527_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='root',
            field=models.ForeignKey(default=1, to='blogging.Post'),
            preserve_default=False,
        ),
    ]
