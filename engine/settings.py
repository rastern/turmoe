import json
import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from engine.message import Repository



# required in case verbose() is called before settings are read
VERBOSE = False



class Export:
    values = [
        #name, desc
        ('BASE_DIR', 'Namespaces directory'),
        ('NAMESPACE', 'API instance to use'),
        ('WORKING_DIR', 'Local working directory'),

        ('API_BASE_PATH', 'Base URL prefix'),
        ('API_DYNAMIC_URLS', 'Update URLs as namespace foldres change'),
        ('API_DEFAULT_CONTENT_TYPE', 'Default HTTP response content type'),
        ('VERBOSE', 'Verbose mode')
    ]


def _path(path, url=False):
    if url:
        if path[-1] != '/':
            return path + '/'
        return path
    else:
        return os.path.join(path, '')


def verbose(msg):
    if VERBOSE:
        print(msg)


def resolve_namespace_config(workdir):
    try:
        config = os.path.join(workdir, 'namespace.json')

        if not os.path.isfile(config):
            config = 'namespacedefault.json'

        return config
    except Exception as e:
        raise ImproperlyConfigured(f'Error loading namespace configuration file: {e}')


def resolve_working_dir(base, namespace):
    try:
        if not namespace:
            namespace = os.listdir(base)[0]

        return _path(getattr(settings, 'ENGINE_WORKING_DIR',
                     os.path.join(base, namespace))
                    )
    except Exception:
        raise ImproperlyConfigured(f'Unable to locate any API namespace')


def load_namespace_config(config):
    print(f"Loading namespace config '{config}'")

    try:
        with open(config, 'r') as fp:
            data = json.load(fp)

            for k, v in data.items():
                if k in globals():
                    globals()[k] = v
    except FileNotFoundError:
        pass


def update_settings_cache():
    from engine.models import Setting

    for setting in Export.values:
        _value = globals()[setting[0]] if setting[0] in globals() else None
        Setting.objects.update_or_create(
            name=setting[0],
            description=setting[1],
            value=_value,
        )


def load_settings_from_cache():
    for s in Setting.objects.all():
        globals()[s.name] = s.value



API_DYNAMIC_URLS = getattr(settings, 'ENGINE_API_DYNAMIC_URLS', False)
API_BASE_PATH = os.path.join(getattr(settings, 'ENGINE_API_BASE_PATH', 'vmturbo/rest').strip('/\\'), '')
API_DEFAULT_CONTENT_TYPE = getattr(settings, 'ENGINE_API_DEFAULT_CONTENT_TYPE', 'application/json')

BASE_DIR = getattr(settings, 'ENGINE_BASE_DIR', 'namespaces').strip('/\\')
NAMESPACE = getattr(settings, 'ENGINE_NAMESPACE', None)
MESSAGE_DEBUG = getattr(settings, 'ENGINE_MESSAGE_DEBUG', False)
VERBOSE = getattr(settings, 'ENGINE_VERBOSE', False)
WORKING_DIR = resolve_working_dir(BASE_DIR, NAMESPACE)
NAMESPACE_CONFIG = resolve_namespace_config(WORKING_DIR)
MESSAGE_REPOSITORY = Repository(debug=MESSAGE_DEBUG)

load_namespace_config(NAMESPACE_CONFIG)

# fix paths incase namespace configs are malformed
API_BASE_PATH = _path(API_BASE_PATH, True)
API_STATE = {}
