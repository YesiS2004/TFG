
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .models import Marca, Modelo
from .forms import MarcaForm, ModeloForm


# MARCAS

@login_required
def lista_marcas(request):
    busqueda = request.GET.get('q', '').strip()

    marcas = Marca.objects.all().order_by('nombre_marca')

    if busqueda:
        marcas = marcas.filter(
            nombre_marca__icontains=busqueda
        )

    pagina = Paginator(marcas, 10).get_page(
        request.GET.get('page')
    )

    return render(
        request,
        'caracteristicas_vehiculos/lista_marcas.html',
        {
            'pagina': pagina,
            'busqueda': busqueda,
        }
    )


@login_required
def registrar_marca(request):
    if request.method == 'POST':
        form = MarcaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Marca agregada con éxito.')
            return redirect('lista_marcas')
    else:
        form = MarcaForm()

    return render(
        request,
        'caracteristicas_vehiculos/formulario_marca.html',
        {
            'form': form,
            'titulo': 'Registrar marca',
            'texto_boton': 'Guardar marca',
        }
    )


@login_required
def editar_marca(request, pk):
    marca = get_object_or_404(Marca, pk=pk)

    if request.method == 'POST':
        form = MarcaForm(request.POST, instance=marca)

        if form.is_valid():
            form.save()
            messages.success(request, 'Modificación exitosa.')
            return redirect('lista_marcas')
    else:
        form = MarcaForm(instance=marca)

    return render(
        request,
        'caracteristicas_vehiculos/formulario_marca.html',
        {
            'form': form,
            'titulo': 'Modificar marca',
            'texto_boton': 'Guardar cambios',
        }
    )


# MODELOS

@login_required
def lista_modelos(request):
    busqueda = request.GET.get('q', '').strip()

    modelos = Modelo.objects.select_related('marca').all().order_by(
        'marca__nombre_marca',
        'nombre_modelo'
    )

    if busqueda:
        modelos = modelos.filter(
            Q(nombre_modelo__icontains=busqueda) |
            Q(marca__nombre_marca__icontains=busqueda)
        )

    pagina = Paginator(modelos, 10).get_page(
        request.GET.get('page')
    )

    return render(
        request,
        'caracteristicas_vehiculos/lista_modelos.html',
        {
            'pagina': pagina,
            'busqueda': busqueda,
        }
    )


@login_required
def registrar_modelo(request):
    if request.method == 'POST':
        form = ModeloForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Modelo agregado con éxito.')
            return redirect('lista_modelos')
    else:
        form = ModeloForm()

    return render(
        request,
        'caracteristicas_vehiculos/formulario_modelo.html',
        {
            'form': form,
            'titulo': 'Registrar modelo',
            'texto_boton': 'Guardar modelo',
            'hay_marcas': Marca.objects.exists(),
        }
    )


@login_required
def editar_modelo(request, pk):
    modelo = get_object_or_404(Modelo, pk=pk)

    if request.method == 'POST':
        form = ModeloForm(request.POST, instance=modelo)

        if form.is_valid():
            form.save()
            messages.success(request, 'Modificación exitosa.')
            return redirect('lista_modelos')
    else:
        form = ModeloForm(instance=modelo)

    return render(
        request,
        'caracteristicas_vehiculos/formulario_modelo.html',
        {
            'form': form,
            'titulo': 'Modificar modelo',
            'texto_boton': 'Guardar cambios',
            'hay_marcas': Marca.objects.exists(),
        }
    )
