from django.contrib import admin
from orderapp.models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'client', 'session_key')


admin.site.register(Order, OrderAdmin)
