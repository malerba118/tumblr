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
        return reverse("blog", self.slug)

    def isOwnedBy(self, usr):
        return self.user == usr



class Post(models.Model):
    blog = models.OneToOneField(Blog)
    root = models.ForeignKey("self")
    timestamp = models.DateTimeField(auto_now_add = True)
    title = models.CharField(max_length=100)
    content = models.TextField()

