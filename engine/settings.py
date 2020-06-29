import json
import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from engine.message import Repository



class Export:
    values = [
        #name, desc
        ('BASE_DIR', 'Namespaces directory'),
        ('NAMESPACE', 'API instance to use'),
        ('WORKING_DIR', 'Local working directory'),

        ('API_BASE_PATH', 'Base URL prefix'),
        ('API_DYNAMIC_URLS', 'Update URLs as namespace foldres change'),
        ('API_DEFAULT_CONTENT_TYPE', 'Default HTTP response content type'),
    ]


def path_trailing_slash(path, url=False):
    if url:
        if path[-1] != '/':
            return path + '/'
        return path
    else:
        return os.path.join(path, '')


def resolve_namespace_config(workdir):
    try:
        config = os.path.join(workdir, 'config.json')

        if not os.path.isfile(config):
            config = 'namespacedefault.json'

        return config
    except Exception as e:
        raise ImproperlyConfigured(f'Error loading namespace configuration file: {e}')


def resolve_working_dir(base, namespace):
    try:
        if not namespace:
            namespace = os.listdir(base)[0]

        return path_trailing_slash(getattr(settings, 'ENGINE_WORKING_DIR',
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


def load_state():
    from engine.models import State

    API_STATE = {}

    for row in State.objects.all():
        if row.value.lower() not in ['null', 'none']:
            API_STATE[row.name] = row.value
        else:
            del API_STATE[row.name]


def get_state(name):
    return API_STATE.get(name.lower(), None)


def update_state(name=None, value=None):
    from engine.models import State

    name = name.lower()

    if name:
        if value is not None or \
        (isinstance(value, str) and value.lower() not in ['null', 'none']):
            API_STATE[name] = value
            State.objects.update_or_create(name=name, defaults={'value': value})
        else:
            del API_STATE[name]
            State.objects.filter(name=name).delete()
    else:
        for key in API_STATE:
            State.objects.update_or_create(name=name, defaults={'value': API_STATE[name]})



API_DYNAMIC_URLS = getattr(settings, 'ENGINE_API_DYNAMIC_URLS', False)
API_BASE_PATH = os.path.join(getattr(settings, 'ENGINE_API_BASE_PATH', 'vmturbo/rest').strip('/\\'), '')
API_DEFAULT_CONTENT_TYPE = getattr(settings, 'ENGINE_API_DEFAULT_CONTENT_TYPE', 'application/json')

BASE_DIR = getattr(settings, 'ENGINE_BASE_DIR', 'namespaces').strip('/\\')
NAMESPACE = getattr(settings, 'ENGINE_NAMESPACE', None)
MESSAGE_DEBUG = getattr(settings, 'ENGINE_MESSAGE_DEBUG', False)
WORKING_DIR = resolve_working_dir(BASE_DIR, NAMESPACE)
NAMESPACE_CONFIG = resolve_namespace_config(WORKING_DIR)
MESSAGE_REPOSITORY = Repository(debug=MESSAGE_DEBUG)

load_namespace_config(NAMESPACE_CONFIG)

# fix paths incase namespace configs are malformed
API_BASE_PATH = path_trailing_slash(API_BASE_PATH, True)
API_STATE = {}
