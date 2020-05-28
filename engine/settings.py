import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured



PROJECT_DIR = '..'

BASE_DIR = getattr(settings, 'ENGINE_BASE_DIR', 'namespaces').strip('/')
NAMESPACE = getattr(settings, 'ENGINE_NAMESPACE', None)

try:
    if not NAMESPACE:
        NAMESPACE = os.listdir(BASE_DIR)[0]

    WORKING_DIR = os.path.join(BASE_DIR, NAMESPACE)
except Exception:
    raise ImproperlyConfigured(f'Unable to locate API namespace "{NAMESPACE}"')

TURBO_BASE_PATH = os.path.join(getattr(settings, 'ENGINE_TURBO_BASE_PATH', 'api/v2').strip('/\\'), '')
