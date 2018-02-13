from django.shortcuts import redirect
from wrapt import decorator


@decorator
def check_authenticated(wrapped, instance, args, kwargs):
    request = instance.request
    if not request.user.is_authenticated():
        return redirect('/login/')
    return wrapped(*args, **kwargs)
