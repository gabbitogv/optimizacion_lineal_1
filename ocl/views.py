from django.shortcuts import render
from .models import Almacen
# Create your views here.


def calcular(request):

    if request.method == 'GET':
        lista = Almacen.objects.all()

        return render(request, 'templates/calculo.html', {'listado': lista})
