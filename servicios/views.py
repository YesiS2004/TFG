
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Servicio
from .forms import ServicioForm


@login_required
def lista_servicios(request):
    busqueda = request.GET.get('q', '').strip()

    servicios = Servicio.objects.all()

    if busqueda:
        servicios = servicios.filter(
            Q(nombre__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )

    paginator = Paginator(servicios, 10)
    pagina = paginator.get_page(request.GET.get('page'))

    return render(request, 'servicios/lista_servicios.html', {
        'pagina': pagina,
        'busqueda': busqueda,
    })


@login_required
def registrar_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request, 'Servicio agregado con éxito.'
            )
            return redirect('lista_servicios')
    else:
        form = ServicioForm()

    return render(request, 'servicios/registrar_servicio.html', {
        'form': form,
        'titulo': 'Registrar servicio',
        'texto_boton': 'Guardar servicio',
    })


@login_required
def editar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)

    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)

        if form.is_valid():
            form.save()
            messages.success(
                request, 'Modificación exitosa.'
            )
            return redirect('lista_servicios')
    else:
        form = ServicioForm(instance=servicio)

    return render(request, 'servicios/registrar_servicio.html', {
        'form': form,
        'titulo': 'Editar servicio',
        'texto_boton': 'Guardar cambios',
    })


@login_required
@require_POST
def eliminar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    servicio.delete()

    messages.success(
        request, 'Servicio eliminado con éxito.'
    )

    return redirect('lista_servicios')
