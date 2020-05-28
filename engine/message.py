import os

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import yaml
from engine import settings



def to_meta_key(name):
    name = name.replace('-', '_').upper()

    if name in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
        return name
    else:
        return f'HTTP_{name}'


def read(file):
    with open(file, 'r') as fp:
        return yaml.load(fp, Loader=Loader)


def match(request, resource):
    # method
    if request.method.upper() != resource['request']['method'].upper():
        return False

    # see https://docs.djangoproject.com/en/1.10/ref/request-response/#django.http.HttpRequest.META
    # for limitations regarding header translation
    for key, value in resource['request'].get('headers', dict()).items():
        try:
            if not value == request.META[to_meta_key(key)]:
                return False
        except KeyError:
            return False

    # parameters
    for key, value in resource['request'].get('parameters', dict()).items():
        if key not in request.GET:
            return False

        try:
            if value != request.GET[key]:
                return False
        except TypeError:
            if value not in request.GET[key]:
                return False

    # data
    if request.method.upper() in ('POST', 'PUT'):
        if request.body.decode().replace('\n', '').strip() != \
        resource['request'].get('body', '').replace('\n', '').strip():
            return False

    return True


def find(request):
    relpath = os.path.join(settings.WORKING_DIR,
                 request.path.strip('/').replace(settings.TURBO_BASE_PATH, ''))

    for root, dirs, files in os.walk(relpath):
        if files:
            for file_ in files:
                data = read(os.path.join(root, file_))
                if match(request, data):
                    return data['response']
    return False
