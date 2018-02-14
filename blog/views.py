from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views.generic import CreateView, View, list

from .models import Post, Profile
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
        queryset = Post.objects.all()
        if self._is_authenticated():
            queryset = self.get_queryset_impl(queryset)
        return queryset

    def get_queryset_impl(self, queryset):
        user = self.request.user.profile
        if self.filter == 'my':
            queryset = queryset.filter(user_profile=user)
        elif self.filter == 'subscription':
            queryset = queryset.filter(user_profile__in=user.subscription.all())
        if user.viewed:
            queryset = queryset.exclude(pk__in=user.viewed)
        return queryset

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
        self.user_id = request.GET.get('user_id', None)
        self.post_id = request.GET.get('post_id', None)
        return super(PostsActions, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = request.user.profile
        sub_user = Profile.objects.get(pk=self.user_id) if self.user_id else None
        if self.action == 'subscriptions':
            if sub_user not in user.subscription.all() and sub_user != user:
                user.subscription.add(Profile.objects.get(pk=self.user_id))
                user.save()
        elif self.action == 'hide':
            if self.post_id not in user.viewed:
                user.viewed.append(self.post_id)
                user.save()
        elif self.action == 'unsubscribe':
            if sub_user in user.subscription.all():
                user.subscription.remove(Profile.objects.get(pk=self.user_id))
                user.save()
        return redirect('/')
