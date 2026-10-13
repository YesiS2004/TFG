
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Cliente
from .forms import ClienteForm
from django.contrib import messages
from django.db.models import Q

@login_required
def lista_clientes(request):
    busqueda = request.GET.get('q', '').strip()

    clientes = Cliente.objects.all()

    if busqueda:
        clientes = clientes.filter(
            Q(documento__icontains=busqueda) |
            Q(nombre__icontains=busqueda) |
            Q(apellido__icontains=busqueda)
        )

    paginator = Paginator(clientes, 10)
    pagina = paginator.get_page(request.GET.get('page'))

    return render(request, 'clientes/lista_clientes.html', {
        'pagina': pagina,
        'busqueda': busqueda,
    })

@login_required
def registrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente agregado con éxito')
            return redirect('lista_clientes')
    else:
        form = ClienteForm()

    return render(request, 'clientes/registrar_cliente.html', {
        'form': form,
        'titulo': 'Registrar cliente',
        'texto_boton': 'Guardar cliente',
    })

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)

        if form.is_valid():
            form.save()
            messages.success(request, 'Datos del cliente modificados con éxito')
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'clientes/registrar_cliente.html', {
        'form': form,
        'titulo': 'Editar cliente',
        'texto_boton': 'Guardar cambios',
    })


@require_POST
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    messages.success(request, 'Cliente eliminado con éxito')
    return redirect('lista_clientes')
