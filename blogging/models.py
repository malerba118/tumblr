from django.contrib.auth.models import User
from django.contrib.contenttypes.generic import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models


# Create your models here.
from django.utils.text import slugify




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






class Blog(models.Model):
    user = models.OneToOneField(User)
    title = models.CharField(max_length=100, default="Dooood, give your blog a title")
    description = models.CharField(max_length=500, default="Look at me, I'm a description, weeee (hell yes, that even rhymes).")
    template = models.CharField(max_length=100, default="default_blog_template.html")
    slug = models.SlugField(unique = True)

    def get_absolute_url(self):
        return reverse("blog", kwargs={"slug":self.slug})

    def isOwnedBy(self, usr):
        return self.user == usr

    def get_posts(self):
        return Post.objects.filter(blog = self).order_by("-timestamp")

    def is_following(self, blog):
        return Follow.objects.filter(follower=self, followee=blog).count() != 0

    """
    Create and persist a follow object where this blog follows a blog
    that is passed as an argument.
    @:param blog - blog to be followed
    """
    def follow(self, blog):
        f = Follow()
        f.follower = self
        f.followee = blog
        f.save()
        return f

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
        activities = Activity.objects.filter(subject__in=followers, activity_type__in=[POST, REBLOG])
        return activities

class Tag(models.Model):
    tag = models.CharField(max_length=50)

    @staticmethod
    def find_or_create_tags(string):
        tags = []
        words = string.split(",")
        for word in words:
            sluggified_word = slugify(word)
            if sluggified_word != '':
                if Tag.objects.filter(tag=sluggified_word).count() > 0:
                    tags.append(Tag.objects.get(tag=sluggified_word))
                else:
                    tag = Tag()
                    tag.tag = sluggified_word
                    tag.save()
                    tags.append(tag)
        return tags

    @staticmethod
    def find_posts_for_tag(tag):
        try:
            qs = Tag.objects.get(tag=tag)
        except Tag.DoesNotExist:
            return []

        return qs.post_set.order_by("-timestamp").all()


class Post(models.Model):
    blog = models.ForeignKey(Blog)
    root = models.ForeignKey("self", null=True)
    timestamp = models.DateTimeField(auto_now_add = True)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    activity = GenericRelation(Activity, content_type_field="content_type", object_id_field="object_fk")

    def find_notes(self):
        return Post.objects.filter(root=self.root).exclude(pk=self.root.pk).order_by("-timestamp")

    def find_likes(self):
        return Like.objects.filter(liked=self).order_by("-timestamp")

    def is_liked_by(self, blog):
        return Like.objects.filter(liker=blog, liked=self).count() > 0



class Follow(models.Model):
    follower = models.ForeignKey(Blog, related_name="follower")
    followee = models.ForeignKey(Blog, related_name="followee")
    timestamp = models.DateTimeField(auto_now_add=True)
    activity = GenericRelation(Activity, content_type_field="content_type", object_id_field="object_fk")

class Like(models.Model):
    liker = models.ForeignKey(Blog)
    liked = models.ForeignKey(Post)
    timestamp = models.DateTimeField(auto_now_add=True)
    activity = GenericRelation(Activity, content_type_field="content_type", object_id_field="object_fk")
