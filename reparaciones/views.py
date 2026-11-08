
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import transaction

from .models import Reparacion, ReparacionRepuesto, ReparacionServicio
from .forms import ReparacionForm

from repuestos.models import Repuesto
from servicios.models import Servicio


def lista_reparaciones(request):
    busqueda = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()

    reparaciones = Reparacion.objects.select_related(
        'vehiculo__cliente',
        'vehiculo__modelo__marca',
        'vehiculo__color'
    ).prefetch_related(
        'repuestos_utilizados__repuesto',
        'servicios_realizados__servicio'
    ).all()

    if busqueda:
        reparaciones = reparaciones.filter(
            Q(vehiculo__cliente__nombre__icontains=busqueda) |
            Q(vehiculo__cliente__apellido__icontains=busqueda) |
            Q(vehiculo__matricula__icontains=busqueda) |
            Q(vehiculo__modelo__nombre_modelo__icontains=busqueda) |
            Q(vehiculo__modelo__marca__nombre_marca__icontains=busqueda)
        )

    if estado:
        reparaciones = reparaciones.filter(estado=estado)

    paginador = Paginator(reparaciones, 10)
    pagina = paginador.get_page(request.GET.get('page'))

    return render(request, 'reparaciones/lista_reparaciones.html', {
        'pagina': pagina,
        'busqueda': busqueda,
        'estado_seleccionado': estado,
        'estados': Reparacion.ESTADOS,
    })


def leer_carrito(formulario):
    try:
        servicios = json.loads(
            formulario.cleaned_data.get('servicios_data') or '[]'
        )
        repuestos = json.loads(
            formulario.cleaned_data.get('repuestos_data') or '[]'
        )
    except (json.JSONDecodeError, TypeError):
        raise ValueError('Los datos del carrito no son válidos.')

    if not isinstance(servicios, list) or not isinstance(repuestos, list):
        raise ValueError('Los datos del carrito no son válidos.')

    try:
        servicios_ids = [int(item) for item in servicios]

        repuestos_cantidades = {}
        for item in repuestos:
            identificador = int(item['id'])
            cantidad = int(item['cantidad'])

            if cantidad < 1:
                raise ValueError('Las cantidades deben ser mayores que cero.')

            if identificador in repuestos_cantidades:
                raise ValueError('Hay repuestos duplicados en el carrito.')

            repuestos_cantidades[identificador] = cantidad

    except (ValueError, TypeError, KeyError):
        raise ValueError('Revisa los servicios y repuestos seleccionados.')

    if len(servicios_ids) != len(set(servicios_ids)):
        raise ValueError('Hay servicios duplicados en el carrito.')

    return servicios_ids, repuestos_cantidades


def guardar_reparacion(formulario, reparacion=None):

    servicios_ids, repuestos_cantidades = leer_carrito(formulario)

    with transaction.atomic():

        # Si estamos editando, devolvemos al stock
        # los repuestos que estaban asociados anteriormente.
        if reparacion and reparacion.pk:

            relaciones_anteriores = list(
                ReparacionRepuesto.objects.filter(
                    reparacion=reparacion
                )
            )

            for relacion in relaciones_anteriores:
                repuesto = Repuesto.objects.select_for_update().get(
                    pk=relacion.repuesto_id
                )

                repuesto.cantidad += relacion.cantidad
                repuesto.save(update_fields=['cantidad'])

        # Verificar que los servicios existan.
        servicios = list(
            Servicio.objects.filter(pk__in=servicios_ids)
        )

        if len(servicios) != len(servicios_ids):
            raise ValueError('Uno o más servicios seleccionados ya no existen.')

        # Bloquear y verificar los repuestos seleccionados.
        repuestos = {
            repuesto.pk: repuesto
            for repuesto in Repuesto.objects.select_for_update().filter(
                pk__in=repuestos_cantidades.keys()
            )
        }

        if len(repuestos) != len(repuestos_cantidades):
            raise ValueError('Uno o más repuestos seleccionados ya no existen.')

        for identificador, cantidad in repuestos_cantidades.items():

            repuesto = repuestos[identificador]

            if cantidad > repuesto.cantidad:
                raise ValueError(
                    f'Stock insuficiente para {repuesto.nombre_pieza}. '
                    f'Disponible: {repuesto.cantidad}.'
                )

        # Guardar la reparación.
        reparacion = formulario.save(commit=False)
        reparacion.save()

        # Reemplazar los repuestos asociados.
        ReparacionRepuesto.objects.filter(
            reparacion=reparacion
        ).delete()

        for identificador, cantidad in repuestos_cantidades.items():

            repuesto = repuestos[identificador]

            ReparacionRepuesto.objects.create(
                reparacion=reparacion,
                repuesto=repuesto,
                cantidad=cantidad
            )

            repuesto.cantidad -= cantidad
            repuesto.save(update_fields=['cantidad'])

        # Reemplazar los servicios asociados.
        ReparacionServicio.objects.filter(
            reparacion=reparacion
        ).delete()

        for servicio in servicios:
            ReparacionServicio.objects.create(
                reparacion=reparacion,
                servicio=servicio
            )

        return reparacion


def datos_formulario(reparacion=None, formulario=None):

    servicios_disponibles = [
        {
            'id': servicio.pk,
            'nombre': servicio.nombre,
            'costo': servicio.costo,
        }
        for servicio in Servicio.objects.all().order_by('nombre')
    ]

    cantidades_anteriores = {}

    if reparacion and reparacion.pk:
        cantidades_anteriores = {
            relacion.repuesto_id: relacion.cantidad
            for relacion in reparacion.repuestos_utilizados.all()
        }

    repuestos_disponibles = [
        {
            'id': repuesto.pk,
            'nombre': repuesto.nombre_pieza,
            'costo': repuesto.costo,
            'stock': repuesto.cantidad + cantidades_anteriores.get(
                repuesto.pk, 0
            ),
        }
        for repuesto in Repuesto.objects.all().order_by('nombre_pieza')
    ]

    carrito_servicios = []
    carrito_repuestos = []

    if formulario and formulario.is_bound:

        try:
            carrito_servicios = json.loads(
                formulario.data.get('servicios_data') or '[]'
            )
            carrito_repuestos = json.loads(
                formulario.data.get('repuestos_data') or '[]'
            )
        except (json.JSONDecodeError, TypeError):
            pass

    elif reparacion and reparacion.pk:

        carrito_servicios = [
            {
                'id': relacion.servicio_id,
                'nombre': relacion.servicio.nombre,
                'costo': relacion.servicio.costo,
            }
            for relacion in reparacion.servicios_realizados.select_related(
                'servicio'
            )
        ]

        carrito_repuestos = [
            {
                'id': relacion.repuesto_id,
                'nombre': relacion.repuesto.nombre_pieza,
                'costo': relacion.repuesto.costo,
                'cantidad': relacion.cantidad,
            }
            for relacion in reparacion.repuestos_utilizados.select_related(
                'repuesto'
            )
        ]

    return {
        'servicios_disponibles': servicios_disponibles,
        'repuestos_disponibles': repuestos_disponibles,
        'carrito_servicios': carrito_servicios,
        'carrito_repuestos': carrito_repuestos,
    }


def registrar_reparacion(request):

    if request.method == 'POST':
        formulario = ReparacionForm(request.POST)

        if formulario.is_valid():
            try:
                guardar_reparacion(formulario)
                messages.success(request, 'Reparación registrada con éxito.')
                return redirect('lista_reparaciones')

            except ValueError as error:
                formulario.add_error(None, str(error))

    else:
        formulario = ReparacionForm()

    contexto = datos_formulario(formulario=formulario)

    return render(request, 'reparaciones/registrar_reparacion.html', {
        'formulario': formulario,
        **contexto,
    })


def editar_reparacion(request, pk):

    reparacion = get_object_or_404(Reparacion, pk=pk)

    if request.method == 'POST':
        formulario = ReparacionForm(
            request.POST,
            instance=reparacion
        )

        if formulario.is_valid():
            try:
                guardar_reparacion(formulario, reparacion)
                messages.success(request, 'Modificación exitosa.')
                return redirect('lista_reparaciones')

            except ValueError as error:
                formulario.add_error(None, str(error))

    else:
        formulario = ReparacionForm(instance=reparacion)

    contexto = datos_formulario(
        reparacion=reparacion,
        formulario=formulario if request.method == 'POST' else None
    )

    return render(request, 'reparaciones/registrar_reparacion.html', {
        'formulario': formulario,
        'reparacion': reparacion,
        **contexto,
    })


def eliminar_reparacion(request, pk):

    reparacion = get_object_or_404(Reparacion, pk=pk)

    if request.method == 'POST':

        with transaction.atomic():

            relaciones = list(
                ReparacionRepuesto.objects.filter(
                    reparacion=reparacion
                )
            )

            for relacion in relaciones:
                repuesto = Repuesto.objects.select_for_update().get(
                    pk=relacion.repuesto_id
                )

                repuesto.cantidad += relacion.cantidad
                repuesto.save(update_fields=['cantidad'])

            reparacion.delete()

        messages.success(request, 'Reparación eliminada con éxito.')

    return redirect('lista_reparaciones')
