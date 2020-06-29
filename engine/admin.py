from django.contrib import admin
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path
from django.views import View
from engine import models as engine_models
from engine import settings as engine_settings



admin.site.site_title = "Turmoe Administration"
admin.site.site_header = "Turbonomic Mocking Engine"
admin.site.index_title = "Engine Administration"



class SettingsModelAdmin(admin.ModelAdmin):
    fields = ('name', 'value', 'description')
    list_display = ['name', 'value', 'description']
    list_display_links = None
    list_editable = ['value']
    ordering = ['id']

    actions = None

    def has_add_permission(self, request):
        return False

    def log_addition(self, *args):
        return

    def log_change(self, *args):
        return

    def log_deletion(self, *args):
        return

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        engine_settings.load_settings_from_cache()

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        engine_settings.load_settings_from_cache()


class StateModelAdmin(admin.ModelAdmin):
    fields = ('name', 'value')
    list_display = ['name', 'value']
    list_display_links = None
    list_editable = ['value']
    ordering = ['name']

    #actions = None

    def has_delete_permission(self, request, obj=None):
        return True

    def log_addition(self, *args):
        return

    def log_change(self, *args):
        return

    def log_deletion(self, *args):
        return

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        engine_settings.load_state()

    def delete_queryset(self, request, queryset):
        super().delete_queryset(request, queryset)
        engine_settings.load_state()

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        engine_settings.load_state()



admin.site.register(engine_models.Setting, SettingsModelAdmin)
admin.site.register(engine_models.State, StateModelAdmin)
