from django.contrib import admin
from ocl.models import Almacen, Tipo, Formato
from import_export.admin import ImportExportModelAdmin
import math
from weasyprint import HTML
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string


def calcular_corte(modeladmin, request, queryset):

    objeto_formato = Formato.objects.get(id=1)
    query = queryset.order_by('-largo')
    listado_ordenado = list(query)
    sumatoria = 0
    x = 0

    #Calculo de los cortes
    for lista in listado_ordenado:
        producto = lista.cantidad * lista.largo
        sumatoria = sumatoria + producto

    division = sumatoria / objeto_formato.formato
    valor_ideal = math.ceil(division)
    listado_corte = []
    largo_listado_ordenado = len(listado_ordenado)

    for i in range(valor_ideal):

        lista_corte = []
        limite = objeto_formato.formato
        corte = True
        indice = 0

        #Ciclo de disponibilidad de material para tiras
        # Ciclo de llenado de tiras
        for lista in listado_ordenado:

            largo = lista.largo + objeto_formato.perdida
            if largo > limite and lista.cantidad > 0:
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
                    limite = limite - disponibilidad * largo

                elif division < disponibilidad:
                    diferencia = disponibilidad - division
                    for i in range(division):
                        lista_corte.append(largo)
                    lista.cantidad = diferencia
                    limite = limite - division * largo
            if indice == len(listado_ordenado)-1:
                listado_corte.append(lista_corte)
                break

            indice = indice+1

    html_string = render_to_string('templates/ficha.html', {'valor_ideal': valor_ideal, 'lista': listado_corte})
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    html.write_pdf(target='/home/cerbeerza/Documentos/ficha.pdf')
    fs = FileSystemStorage('/home/cerbeerza/Documentos')
    with fs.open('ficha.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="ficha.pdf"'
        return response


calcular_corte.short_description = 'Calculo de Corte'


class AlmacenAdmin(ImportExportModelAdmin):
    list_display = ('tipo', 'largo', 'cantidad')
    actions = [calcular_corte]
    list_filter = ('tipo',)

# Register your models here.


admin.site.register(Almacen, AlmacenAdmin)
admin.site.register(Tipo)
admin.site.register(Formato)
