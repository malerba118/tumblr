from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.



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




class Post(models.Model):
    blog = models.ForeignKey(Blog)
    root = models.ForeignKey("self", null=True)
    timestamp = models.DateTimeField(auto_now_add = True)
    title = models.CharField(max_length=100)
    content = models.TextField()

    def set_root(self, reblogged_post):
        if reblogged_post.root == None:
            self.root = reblogged_post
        else:
            self.root = reblogged_post.root



class Follow(models.Model):
    follower = models.ForeignKey(Blog, related_name="follower")
    followee = models.ForeignKey(Blog, related_name="followee")
    timestamp = models.DateTimeField(auto_now_add=True)