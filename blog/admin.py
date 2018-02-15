from django.contrib import admin

from .models import Post, Profile

# TODO customize the view of models
admin.site.register(Post)
admin.site.register(Profile)
