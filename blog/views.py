from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views.generic import View, list, CreateView

from .models import Post


class PostViews(list.ListView):
    model = Post
    context_object_name = 'posts'

    def get_template_names(self):
        auth = self.request.user.is_authenticated()
        return 'user_posts.html' if auth else 'all_posts.html'

    def get_queryset(self):
        return Post.objects.all()


class LoginViews(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request, onsuccess='/', onfail='/login/'):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect(onsuccess)
        else:
            return redirect(onfail)


class CreatePostViews(CreateView):
    model = Post
    template_name = 'create_post.html'
    fields = ['title', 'text']

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect('/login/')
        try:
            result = request.POST
            Post.objects.create(
                title=result['title'],
                text=result['text'],
                user_profile=request.user.profile
            )
            return redirect('/')
        except:
            return redirect('/create_post/')
