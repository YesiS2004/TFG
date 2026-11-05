
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Repuesto
from .forms import RepuestoForm


# LISTAR REPUESTOS
@login_required
def lista_repuestos(request):
    busqueda = request.GET.get('q', '').strip()

    repuestos = Repuesto.objects.all().order_by('nombre_pieza')

    if busqueda:
        repuestos = repuestos.filter(
            Q(nombre_pieza__icontains=busqueda)
        )

    pagina = Paginator(repuestos, 10).get_page(request.GET.get('page'))

    return render(request, 'repuestos/lista_repuestos.html', {
        'pagina': pagina,
        'busqueda': busqueda,
    })


# REGISTRAR REPUESTO
@login_required
def registrar_repuesto(request):
    if request.method == 'POST':
        form = RepuestoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Repuesto agregado con éxito.')
            return redirect('lista_repuestos')

    else:
        form = RepuestoForm()

    return render(request, 'repuestos/formulario_repuesto.html', {
        'form': form,
        'titulo': 'Registrar repuesto',
        'texto_boton': 'Guardar repuesto',
    })


# EDITAR REPUESTO
@login_required
def editar_repuesto(request, pk):
    repuesto = get_object_or_404(Repuesto, pk=pk)

    if request.method == 'POST':
        form = RepuestoForm(request.POST, instance=repuesto)

        if form.is_valid():
            form.save()
            messages.success(request, 'Modificación exitosa.')
            return redirect('lista_repuestos')

    else:
        form = RepuestoForm(instance=repuesto)

    return render(request, 'repuestos/formulario_repuesto.html', {
        'form': form,
        'titulo': 'Modificar repuesto',
        'texto_boton': 'Guardar cambios',
    })


# ELIMINAR REPUESTO
@login_required
@require_POST
def eliminar_repuesto(request, pk):
    repuesto = get_object_or_404(Repuesto, pk=pk)
    repuesto.delete()

    messages.success(request, 'Repuesto eliminado con éxito.')

    return redirect('lista_repuestos')
