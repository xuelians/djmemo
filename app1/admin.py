from django.contrib import admin

# Register your models here.
from .models import (Config, Category, Tag, Blog, Memo,
                     Chapter, Section, SectionType, Bug, Task, TaskUpdate)


class ConfigAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # if there's already an entry, do not allow adding
        return not Config.objects.exists()


admin.site.register(Config, ConfigAdmin)
admin.site.register([Category, Tag, Blog, Memo,
                     Chapter, Section, SectionType, Bug, Task, TaskUpdate])
