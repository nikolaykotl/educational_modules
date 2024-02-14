from django.contrib import admin

from module.models import Module


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner')
    list_filter = ('owner',)
    search_fields = ('name',)
