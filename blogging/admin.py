from django.contrib import admin

# Register your models here.
from blogging.models import Post, Follow

admin.site.register(Post)
admin.site.register(Follow)
