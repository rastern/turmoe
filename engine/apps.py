import sys

from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig
from engine import settings



class EngineConfig(AppConfig):
    name = 'engine'
    verbose_name = 'API Mocking Engine'
