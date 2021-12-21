from django.contrib import admin

from cartapp.models import Service, ServiceType, UserTypeForServiceType, Cart, CartService, DaysOfWeek, WindowWashing


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'service_type', 'basic_service')


class ServiceTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class CartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'owner', 'session_key', 'total_price', 'in_order')


class CartServiceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'cart')


class WindowWashingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'cart')


admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceType, ServiceTypeAdmin)
admin.site.register(UserTypeForServiceType)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartService, CartServiceAdmin)
admin.site.register(DaysOfWeek)
admin.site.register(WindowWashing, WindowWashingAdmin)
