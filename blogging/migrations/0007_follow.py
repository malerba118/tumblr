# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0006_auto_20150527_2330'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('followee', models.ForeignKey(related_name='followee', to='blogging.Blog')),
                ('follower', models.ForeignKey(related_name='follower', to='blogging.Blog')),
            ],
        ),
    ]
