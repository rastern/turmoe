import os

from django.urls import path
from django.conf import settings as site_settings
from django.urls import include, path
from engine import settings as engine_settings
from engine import views
from engine.autolist import AutoList



def urls():
    urls = []

    for root, dirs, files in os.walk(engine_settings.WORKING_DIR):
        if files:
            if engine_settings.TURBO_DYNAMIC_URLS:
                base = engine_settings.TURBO_BASE_PATH
            else:
                base = ''

            path_ = os.path.join(base,
                    os.path.relpath(root, engine_settings.WORKING_DIR))
            urls.append(path(path_, views.ApiView.as_view()))

    if engine_settings.TURBO_DYNAMIC_URLS and site_settings.DEBUG:
        import debug_toolbar
        urls.append(path('__debug__/', include(debug_toolbar.urls)))

    return urls


# pattern discovery
app_name = 'engine'

if engine_settings.TURBO_DYNAMIC_URLS:
    urlpatterns = AutoList(urls)
else:
    urlpatterns = urls()
