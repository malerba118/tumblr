# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default='Dooood, give your blog a title', max_length=100)),
                ('description', models.CharField(default="Look at me, I'm a description, weeee (hell yes, that even rhymes).", max_length=500)),
                ('template', models.CharField(default='default_blog_template.html', max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
