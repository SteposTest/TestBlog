from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views.generic import View, list

from .models import Post


class PostViews(list.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts.html'

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
