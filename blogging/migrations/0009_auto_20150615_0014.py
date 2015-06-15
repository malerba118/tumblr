# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0008_auto_20150615_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=sorl.thumbnail.fields.ImageField(default='blog_pictures/default.jpg', upload_to='blog_pictures/', blank=True),
        ),
    ]
