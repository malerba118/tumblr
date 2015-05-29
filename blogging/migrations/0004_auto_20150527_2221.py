# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0003_auto_20150527_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog',
            field=models.ForeignKey(to='blogging.Blog'),
        ),
    ]
