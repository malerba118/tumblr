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
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('followee', models.ForeignKey(related_name='followee', to='blogging.Blog')),
                ('follower', models.ForeignKey(related_name='follower', to='blogging.Blog')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('content', models.TextField()),
                ('blog', models.ForeignKey(to='blogging.Blog')),
                ('root', models.ForeignKey(to='blogging.Post', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='blogging.Tag'),
        ),
        migrations.AddField(
            model_name='like',
            name='liked',
            field=models.ForeignKey(to='blogging.Post'),
        ),
        migrations.AddField(
            model_name='like',
            name='liker',
            field=models.ForeignKey(to='blogging.Blog'),
        ),
    ]
