from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from blogging.models import Blog, Follow, Post
# Create your models here.



POST = 0
REBLOG = 1
LIKE = 2
COMMENT = 3
FOLLOW = 4

ACTIVITY_TYPE = (
    (POST, "Post"),
    (REBLOG, "Reblog"),
    (LIKE, "Like"),
    (COMMENT, "Comment"),
    (FOLLOW, "Follow"),
)

class Activity(models.Model):
    subject = models.ForeignKey(Blog)
    timestamp = models.DateTimeField()
    activity_type = models.SmallIntegerField(choices=ACTIVITY_TYPE)
    content_type = models.ForeignKey(ContentType, null=True)
    object_fk = models.PositiveIntegerField()
    object = GenericForeignKey('content_type', 'object_fk')

    @staticmethod
    def create_activity(subject, object, post_type):
        activity = Activity()
        activity.timestamp = object.timestamp
        activity.subject = subject
        activity.activity_type = post_type
        if post_type == POST:
            activity.content_type = ContentType.objects.get_for_model(Post)
        elif post_type == REBLOG:
            activity.content_type = ContentType.objects.get_for_model(Post)
        #elif post_type == LIKE:
        #    activity.content_type = ContentType.objects.get_for_model(Like)
        elif post_type == FOLLOW:
            activity.content_type = ContentType.objects.get_for_model(Follow)
        #elif post_type == COMMENT:
        #    activity.content_type = ContentType.objects.get_for_model(Comment)
        activity.object_fk = object.pk
        activity.save()

    @staticmethod
    def find_newsfeed_activities(blog):
        follows = Follow.objects.filter(follower=blog)
        followers = []
        for follow in follows:
            followers.append(follow.followee)
        activities = Activity.objects.filter(subject__in=followers, activity_type=POST)
        return activities

