import os
import sys

from django.urls import path
from django.conf import settings as site_settings
from django.urls import include, path, re_path
from engine import settings as engine_settings
from engine import views as engine_views
from engine.message import ResourceConfig
from engine.types import AutoList
from engine.settings import verbose



def urls():
    urls = []
    paths = set()

    for root, dirs, files in os.walk(engine_settings.WORKING_DIR):
        if files:
            # don't include paths unless they have a response definition
            responses = [f for f in files if f.endswith('.yaml')]

            if not any(responses):
                continue

            for file_ in responses:
                leaf = ''
                file_path = os.path.join(root, file_)
                res = ResourceConfig(file_path)

                if getattr(res.request, 'path', None):
                    leaf = res.request.path

                path_ = os.path.join(root, leaf).replace(
                                                engine_settings.WORKING_DIR,
                                                engine_settings.API_BASE_PATH
                                                )

                paths.add(path_)
                engine_settings.MESSAGE_REPOSITORY.add(path_, file_path)

    for path_ in paths:
        verbose(f"Appending path: {path_}")
        urls.append(re_path(f"{path_.rstrip('/')}/?", engine_views.MockResponseView.as_view()))

    if engine_settings.API_DYNAMIC_URLS and site_settings.DEBUG:
        import debug_toolbar
        urls.append(path('__debug__/', include(debug_toolbar.urls)))

    return urls


# pattern discovery
app_name = 'engine'

if sys.argv[1] == 'runserver':
    if engine_settings.API_DYNAMIC_URLS:
        verbose("Enabling dynamic URLs")
        urlpatterns = AutoList(urls)
    else:
        verbose("Processing standard URLs")
        urlpatterns = urls()
else:
    urlpatterns = ''
