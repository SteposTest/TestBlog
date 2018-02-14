import os
from importlib import import_module

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_blog.settings")

application = get_wsgi_application()

import_module('blog.utils.models_signal_utils')

create_test_db = os.environ['TEST_DB']
if create_test_db:
    import_module('blog.utils.test_db').create_db()
