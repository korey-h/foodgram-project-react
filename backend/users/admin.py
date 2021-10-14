from django.contrib import admin

from .models import Subscribe


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription')
    search_fields = ('user', 'subscription')
    list_filter = ('user', 'subscription')
    empty_value_display = '-пусто-'


admin.site.register(Subscribe, SubscribeAdmin)
