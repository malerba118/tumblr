from django.contrib import admin

# Register your models here.
from blogging.models import Post, Follow, Like, Tag, Activity

admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Tag)
admin.site.register(Activity)
