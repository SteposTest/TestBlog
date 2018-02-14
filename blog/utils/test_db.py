from django.contrib.auth.models import User

from ..models import Post


def create_db():
    users_names = 'test_user'
    password = 'password123'
    post_name = 'test post'
    post_text = 'bla'

    try:
        admin = User.objects.create(username='admin', is_superuser=True, is_staff=True)
        admin.set_password(password)
        admin.save()
    except:
        return

    for i in range(5):
        user = User.objects.create(username=f'{users_names}{i}')
        user.set_password(password)
        user.save()

        for x in range(i):
            Post.objects.create(
                title=f'{post_name}{i}{x}',
                text=post_text*i,
                user_profile=user.profile
            )
