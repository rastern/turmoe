from django.db import models



class CharFieldLower(models.CharField):
    def __init__(self, *args, **kwargs):
        super(CharFieldLower, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


class Setting(models.Model):
    name = models.CharField(max_length=256)
    value = models.CharField(max_length=256)
    description = models.CharField(max_length=256, null=True)

    class Meta:
        app_label = 'engine'


class State(models.Model):
    name = CharFieldLower(max_length=256, unique=True, help_text='Case insensitive. Names must be unique.')
    value = models.CharField(max_length=256)

    class Meta:
        app_label = 'engine'
