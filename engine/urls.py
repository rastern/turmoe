import os

from django.urls import path
from django.conf import settings as site_settings
from django.urls import include, path
from engine import settings as engine_settings
from engine import views



def generate():
    urls = []

    for root, dirs, files in os.walk(engine_settings.WORKING_DIR):
        if files:
            path_ = os.path.join(engine_settings.TURBO_BASE_PATH,
                    os.path.relpath(root, engine_settings.WORKING_DIR))
            urls.append(path(path_, views.ApiView.as_view()))

    return urls


# pattern discovery
app_name = 'engine'

urlpatterns = generate()
