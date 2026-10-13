
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Proveedor
from .forms import ProveedorForm


@login_required
def lista_proveedores(request):
    busqueda = request.GET.get('q', '').strip()

    proveedores = Proveedor.objects.all()

    if busqueda:
        proveedores = proveedores.filter(
            Q(documento__icontains=busqueda) |
            Q(nombre__icontains=busqueda) |
            Q(apellido__icontains=busqueda)
        )

    paginator = Paginator(proveedores, 10)
    pagina = paginator.get_page(request.GET.get('page'))

    return render(request, 'proveedores/lista_proveedores.html', {
        'pagina': pagina,
        'busqueda': busqueda,
    })


@login_required
def registrar_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request, 'Proveedor agregado con éxito.'
            )
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm()

    return render(request, 'proveedores/registrar_proveedor.html', {
        'form': form,
        'titulo': 'Registrar proveedor',
        'texto_boton': 'Guardar proveedor',
    })


@login_required
def editar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)

    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)

        if form.is_valid():
            form.save()
            messages.success(
                request, 'Modificación exitosa.'
            )
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)

    return render(request, 'proveedores/registrar_proveedor.html', {
        'form': form,
        'titulo': 'Editar proveedor',
        'texto_boton': 'Guardar cambios',
    })


@login_required
@require_POST
def eliminar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    proveedor.delete()

    messages.success(
        request, 'Proveedor eliminado con éxito.'
    )

    return redirect('lista_proveedores')
