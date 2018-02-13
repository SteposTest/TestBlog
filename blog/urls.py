from django.conf.urls import url

from .views import LoginViews, PostViews

urlpatterns = [
    url(r'^login/$', LoginViews.as_view(), name='login_views'),
    url(r'^', PostViews.as_view(), name='posts_view')
]
