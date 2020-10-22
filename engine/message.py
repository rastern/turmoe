import os

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import yaml

from engine.state import get_state, update_state



BODY404 = """
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL {} was not found on this server.</p>
</body></html>
"""



class ResourceConfig:
    """Resource configuration
    """
    __slots__ = [
        'source',
        'request',
        'response'
    ]

    def __init__(self, file):
        self.source = file
        self._load_config()

    def _load_config(self):
        with open(self.source, 'r') as fp:
            data = yaml.load(fp, Loader=Loader)

        self.request = Request(**data['request'])
        self.response = Response(**data['response'])

    @staticmethod
    def to_meta_key(name):
        name = name.replace('-', '_').upper()

        if name in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            return name
        else:
            return f'HTTP_{name}'


class Resource:
    """Base Resource
    """
    __slots__ = [
        'body',
        'headers',
        'method',
        'path',
        'state',
        'options',
        '_eq_failure'
    ]

    def __init__(self, **kwargs):
        self._eq_failure = None
        self.options = None

        for k, v in kwargs.items():
            if k == 'state':
                _state = {}

                for _k, _v in v.items():
                    if isinstance(_v, bool):
                        _state[_k.lower()] = 'True' if _v else 'False'
                    else:
                        _state[_k.lower()] = str(_v)

                setattr(self, k, _state)
            if k == 'parameters':
                _param = {}

                for _k, _v in v.items():
                    if not isinstance(_v, list):
                        _v = [_v]

                    _param[_k] = [str(x) for x in _v]

                setattr(self, k, _param)
            else:
                setattr(self, k, v)

    def __eq__(self, other):
        # self = saved config file, other = incoming request (response)
        # method
        if other.method.upper() != self.method.upper():
            self._eq_failure = 'M01'
            return False

        # see https://docs.djangoproject.com/en/1.10/ref/request-response/#django.http.HttpRequest.META
        # for limitations regarding header translation
        try:
            for key, value in self.headers.items():
                try:
                    if value != other.META[self.to_meta_key(key)]:
                        self._eq_failure = 'H01'
                        return False
                except KeyError:
                    self._eq_failure = 'H02'
                    return False
        except AttributeError:
            pass
        except Exception as e:
            print(e)

        # parameters - all parameters MUST match
        if not self.options or not self.options.get('ignore-parameters', False):
            if (bool(other.GET) != bool(getattr(self, 'parameters', None))):
                self._eq_failure = 'P01'
                return False

            for key, value in other.GET.lists():
                try:
                    if value != self.parameters[key]:
                        self._eq_failure = 'P02'
                        return False
                except KeyError:
                    self._eq_failure = 'P03'
                    return False

        # state - request state must be registered and match
        # states are not mutually exclusive, so check if config matches current
        # server state - else other state settings would trigger False
        try:
            for key in self.state:
                if self.state[key] != get_state(key):
                    self._eq_failure = 'S01'
                    return False
        except AttributeError:
            pass
        except Exception as e:
            print(e)

        # data
        if other.method.upper() in ('POST', 'PUT'):
            if not self.options or not self.options.get('ignore-body', False):
                if other.body.decode().replace('\n', '').strip() != \
                getattr(self, 'body', '').replace('\n', '').strip():
                    self._eq_failure = 'D01'
                    return False

        return True


class Request(Resource):
    """Request
    """
    __slots__ = [
        'parameters',
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Response(Resource):
    """Response
    """
    __slots__ = [
        'status_code'
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_state(self):
        if getattr(self, 'state', None):
            for key in self.state:
                update_state(key, self.state[key])


class Repository:
    """Resource repository mapper
    """
    def __init__(self, debug=False):
        self.__dict = {}
        self.__debug = debug

    def get(self, key):
        return self.__dict[key]

    def add(self, key, value):
        key = f"/{key.strip('/')}"

        if key not in self.__dict:
            self.__dict[key] = set()

        self.__dict[key].add(value)

    def match(self, request):
        try:
            for file in self.__dict[request.path.rstrip('/')]:
                config = ResourceConfig(file)

                if config.request == request:
                    print(f"Serving response from '{file}'")
                    return config.response

                if self.__debug:
                    print(f"DEBUG: '{file}' - {config.request._eq_failure}")

        except KeyError:
            pass

        return Response(status_code=404, body=BODY404.format(request.path))
