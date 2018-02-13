from .models import Post
from django.views.generic.list import ListView


class PostViews(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts.html'

    def get_queryset(self):
        return Post.objects.all()
