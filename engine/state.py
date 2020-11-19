# The state engine is imported before Django initializes the applications,
# thus imports need to be done at the time of use, or Django will fail with
# django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet


def load_state():
    from engine.models import State
    from engine.settings import API_STATE

    API_STATE = {}

    for row in State.objects.all():
        if row.value.lower() not in ['null', 'none']:
            API_STATE[row.name] = row.value
        else:
            del API_STATE[row.name]


def get_state(name):
    from engine.settings import API_STATE

    return API_STATE.get(name.lower(), None)


def update_state(name=None, value=None):
    from engine.models import State
    from engine.settings import API_STATE

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
