from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views.generic import CreateView, View, list

from .models import Post
from .utils.views_utils import check_authenticated


class PostViews(list.ListView):
    model = Post
    context_object_name = 'posts'
    filter = None

    def get_template_names(self):
        auth = self.request.user.is_authenticated()
        return 'user_posts.html' if auth else 'all_posts.html'

    def dispatch(self, request, *args, **kwargs):
        self.filter = request.GET.get('filter_info', None)
        return super(PostViews, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.filter is not None:
            return self._get_query()
        return Post.objects.all()

    @check_authenticated
    def _get_query(self):
        user = self.request.user.profile
        if self.filter == '1':
            return Post.objects.filter(user_profile=user)


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

    @check_authenticated
    def post(self, request, *args, **kwargs):
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
