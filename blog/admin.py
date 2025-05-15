from django.contrib import admin
from blog.models import Comment, Like, BookPost



admin.site.register(BookPost)
admin.site.register(Comment)
admin.site.register(Like)


