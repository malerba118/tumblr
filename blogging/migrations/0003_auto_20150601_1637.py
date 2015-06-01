# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0002_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='template',
            field=models.CharField(default='default_blog_template.html', max_length=100, choices=[('default_blog_template.html', 'Default'), ('simple_blog_template.html', 'Simple')]),
        ),
    ]
