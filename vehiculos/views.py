from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Vehiculo
from .forms import VehiculoForm


def lista_vehiculos(request):
    busqueda = request.GET.get('q', '')

    vehiculos = Vehiculo.objects.select_related(
        'cliente',
        'modelo__marca',
        'color'
    ).all()

    if busqueda:
        vehiculos = vehiculos.filter(
            Q(matricula__icontains=busqueda) |
            Q(chasis__icontains=busqueda) |
            Q(cliente__nombre__icontains=busqueda) |
            Q(cliente__apellido__icontains=busqueda) |
            Q(modelo__nombre_modelo__icontains=busqueda) |
            Q(modelo__marca__nombre_marca__icontains=busqueda) |
            Q(color__color__icontains=busqueda)
        )

    paginador = Paginator(vehiculos, 10)
    numero_pagina = request.GET.get('page')
    pagina = paginador.get_page(numero_pagina)

    return render(request, 'vehiculos/lista_vehiculos.html', {
        'pagina': pagina,
        'busqueda': busqueda,
    })


def registrar_vehiculo(request):
    if request.method == 'POST':
        formulario = VehiculoForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Vehículo agregado con éxito.')
            return redirect('lista_vehiculos')

    else:
        formulario = VehiculoForm()

    return render(request, 'vehiculos/registrar_vehiculo.html', {
        'formulario': formulario,
    })


def editar_vehiculo(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)

    if request.method == 'POST':
        formulario = VehiculoForm(request.POST, instance=vehiculo)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Modificación exitosa.')
            return redirect('lista_vehiculos')

    else:
        formulario = VehiculoForm(instance=vehiculo)

    return render(request, 'vehiculos/registrar_vehiculo.html', {
        'formulario': formulario,
        'vehiculo': vehiculo,
    })


def eliminar_vehiculo(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)

    if request.method == 'POST':
        vehiculo.delete()
        messages.success(request, 'Vehículo eliminado con éxito.')

    return redirect('lista_vehiculos')