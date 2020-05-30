import importlib
import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured



def load_config():
    pass



PROJECT_DIR = '..'

BASE_DIR = getattr(settings, 'ENGINE_BASE_DIR', 'namespaces').strip('/')
NAMESPACE = getattr(settings, 'ENGINE_NAMESPACE', None)

try:
    if not NAMESPACE:
        NAMESPACE = os.listdir(BASE_DIR)[0]

    WORKING_DIR = getattr(settings, 'ENGINE_WORKING_DIR',
                          os.path.join(BASE_DIR, NAMESPACE))
except Exception:
    raise ImproperlyConfigured(f'Unable to locate any API namespace')

try:
    config = os.path.join(WORKING_DIR, 'config.py')

    if os.path.isfile(config):
        importlib.import_module(config)
    else:
        import engine.namespacedefault as config

    load_config()
except Exception as e:
    raise ImproperlyConfigured(f'Error loading namespace configuration file: {e}')

TURBO_DYNAMIC_URLS = getattr(settings, 'ENGINE_TURBO_DYNAMIC_URLS', False)
TURBO_BASE_PATH = os.path.join(getattr(settings, 'ENGINE_TURBO_BASE_PATH', 'vmturbo/rest').strip('/\\'), '')
