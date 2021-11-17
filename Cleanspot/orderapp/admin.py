from django.contrib import admin
from orderapp.models import Service, ServiceType, Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'client')


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'service_type')


admin.site.register(Order, OrderAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceType)
admin.site.register(OrderItem)
