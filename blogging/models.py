from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.
from django.utils.text import slugify


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

        return qs.post_set.all()


class Post(models.Model):
    blog = models.ForeignKey(Blog)
    root = models.ForeignKey("self", null=True)
    timestamp = models.DateTimeField(auto_now_add = True)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)

    def find_notes(self):
        return Post.objects.filter(root=self.root)

    def find_likes(self):
        return Like.objects.filter(liked=self)

    def is_liked_by(self, blog):
        return Like.objects.filter(liker=blog, liked=self).count() > 0



class Follow(models.Model):
    follower = models.ForeignKey(Blog, related_name="follower")
    followee = models.ForeignKey(Blog, related_name="followee")
    timestamp = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    liker = models.ForeignKey(Blog)
    liked = models.ForeignKey(Post)
    timestamp = models.DateTimeField(auto_now_add=True)
