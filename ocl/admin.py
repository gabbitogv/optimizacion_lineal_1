from django.contrib import admin
from ocl.models import Almacen, Tipo
from import_export.admin import ImportExportModelAdmin


def algo(modeladmin, request, queryset):

    datos = queryset
    pass


algo.short_description = 'Algo'


class AlmacenAdmin(ImportExportModelAdmin):
    list_display = ('tipo', 'largo', 'cantidad')
    actions = [algo]

# Register your models here.


admin.site.register(Almacen, AlmacenAdmin)
admin.site.register(Tipo)
