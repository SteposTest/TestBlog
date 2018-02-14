from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import CreateView, View, list

from .models import Post
from .utils.views_utils import check_authenticated


class PostViews(list.ListView):
    model = Post
    context_object_name = 'posts'
    filter = None

    def get_template_names(self):
        auth = self._is_authenticated()
        return 'user_posts.html' if auth else 'all_posts.html'

    def dispatch(self, request, *args, **kwargs):
        self.filter = request.GET.get('filter_info', None)
        return super(PostViews, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self._is_authenticated():
            return self.get_queryset_impl()
        return Post.objects.all()

    def get_queryset_impl(self):
        user = self.request.user.profile
        queryset = Post.objects.all()
        if self.filter == '1':
            return queryset.filter(user_profile=user)
        return queryset.exclude(pk__in=user.viewed)

    def _is_authenticated(self):
        return self.request.user.is_authenticated()


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
            return redirect('/?filter_info=1')
        except:
            return redirect('/create_post/')


class PostsActions(View):
    @check_authenticated
    def dispatch(self, request, *args, **kwargs):
        self.action = request.GET.get('action', None)
        self.user_name = request.GET.get('name', None)
        self.post_id = request.GET.get('id', None)
        return super(PostsActions, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = request.user.profile
        if self.action == '1':
            sub_user = User.objects.get(username=self.user_name).profile
        if self.action == '2':
            if self.post_id not in user.viewed:
                user.viewed.append(self.post_id)
                user.save()
        return redirect('/')
