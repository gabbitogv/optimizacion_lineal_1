from django.contrib import admin
from ocl.models import Almacen, Tipo, Formato
from import_export.admin import ImportExportModelAdmin
import math


def calcular_corte(modeladmin, request, queryset):

    objeto_formato = Formato.objects.get(id=1)
    query = queryset.order_by('-largo')
    listado_ordenado = list(query)
    sumatoria = 0

    #Calculo de los cortes
    for lista in listado_ordenado:
        producto = lista.cantidad * lista.largo
        sumatoria = sumatoria + producto

    division = sumatoria / objeto_formato.formato
    valor_ideal = math.ceil(division)
    listado_corte = []

    for i in range(valor_ideal):

        lista_corte = []
        limite = objeto_formato.formato

        for lista in listado_ordenado:
            largo = lista.largo + objeto_formato.perdida
            if largo > limite:
                listado_corte.append(lista_corte)
                break
            disponibilidad = lista.cantidad
            if disponibilidad > 0:
                division = limite / largo
                division = math.floor(division)
                if division >= disponibilidad:
                    for i in range(disponibilidad):
                        lista_corte.append(largo)
                    lista.cantidad = 0

                elif division < disponibilidad:
                    diferencia = disponibilidad - division
                    for i in range(division):
                        lista_corte.append(largo)
                    lista.cantidad = diferencia
                limite = limite - disponibilidad * largo


calcular_corte.short_description = 'Calculo de Corte'


class AlmacenAdmin(ImportExportModelAdmin):
    list_display = ('tipo', 'largo', 'cantidad')
    actions = [calcular_corte]
    list_filter = ('tipo',)

# Register your models here.


admin.site.register(Almacen, AlmacenAdmin)
admin.site.register(Tipo)
admin.site.register(Formato)
