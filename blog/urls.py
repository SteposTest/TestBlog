from django.conf.urls import url

from .views import PostViews

urlpatterns = [
    url(r'^', PostViews.as_view(), name='posts_view')
]
