from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import IntegrityError, transaction

from .models import Turno
from .forms import TurnoForm


def lista_turnos(request):
    busqueda = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()

    turnos = Turno.objects.select_related(
        'cliente',
        'reparacion__vehiculo__cliente',
        'reparacion__vehiculo__modelo__marca'
    ).all()

    if busqueda:
        turnos = turnos.filter(
            Q(cliente__nombre__icontains=busqueda) |
            Q(cliente__apellido__icontains=busqueda) |
            Q(reparacion__vehiculo__matricula__icontains=busqueda) |
            Q(reparacion__vehiculo__modelo__nombre_modelo__icontains=busqueda)
        )

    if estado:
        turnos = turnos.filter(estado=estado)

    paginador = Paginator(turnos, 10)
    pagina = paginador.get_page(request.GET.get('page'))

    return render(request, 'turnos/lista_turnos.html', {
        'pagina': pagina,
        'busqueda': busqueda,
        'estado_seleccionado': estado,
        'estados': Turno.ESTADOS,
    })


def registrar_turno(request):
    if request.method == 'POST':
        formulario = TurnoForm(request.POST)

        if formulario.is_valid():
            try:
                with transaction.atomic():
                    formulario.save()

                messages.success(
                    request,
                    'Turno registrado con éxito.'
                )
                return redirect('lista_turnos')

            except IntegrityError:
                formulario.add_error(
                    None,
                    'Ya existe un turno registrado para esa fecha y hora.'
                )

    else:
        formulario = TurnoForm()

    return render(request, 'turnos/registrar_turno.html', {
        'formulario': formulario,
    })


def editar_turno(request, pk):
    turno = get_object_or_404(Turno, pk=pk)

    if request.method == 'POST':
        formulario = TurnoForm(request.POST, instance=turno)

        if formulario.is_valid():
            try:
                with transaction.atomic():
                    formulario.save()

                messages.success(
                    request,
                    'Modificación exitosa.'
                )
                return redirect('lista_turnos')

            except IntegrityError:
                formulario.add_error(
                    None,
                    'Ya existe un turno registrado para esa fecha y hora.'
                )

    else:
        formulario = TurnoForm(instance=turno)

    return render(request, 'turnos/registrar_turno.html', {
        'formulario': formulario,
        'turno': turno,
    })


def eliminar_turno(request, pk):
    turno = get_object_or_404(Turno, pk=pk)

    if request.method == 'POST':
        turno.delete()

        messages.success(
            request,
            'Turno eliminado con éxito.'
        )

    return redirect('lista_turnos')