from django.contrib import admin
from mainapp.models import Cities, PremisesType, Premises


class PremisesAdmin(admin.ModelAdmin):
    model = Premises
    list_display = ('premises_owner', '__str__')


admin.site.register(Cities)
admin.site.register(PremisesType)
admin.site.register(Premises, PremisesAdmin)
