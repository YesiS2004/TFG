
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q

from .models import Pedido, DetallePedido
from .forms import PedidoForm
from repuestos.models import Repuesto


def lista_pedidos(request):
    busqueda = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()

    pedidos = Pedido.objects.select_related(
        'proveedor'
    ).prefetch_related(
        'detalles__repuesto'
    ).all()

    if busqueda:
        pedidos = pedidos.filter(
            Q(proveedor__nombre__icontains=busqueda) |
            Q(proveedor__apellido__icontains=busqueda) |
            Q(detalles__repuesto__nombre_pieza__icontains=busqueda)
        ).distinct()

    if estado:
        pedidos = pedidos.filter(estado=estado)

    paginador = Paginator(pedidos, 10)
    pagina = paginador.get_page(request.GET.get('page'))

    return render(request, 'pedidos/lista_pedidos.html', {
        'pagina': pagina,
        'busqueda': busqueda,
        'estado_seleccionado': estado,
        'estados': Pedido.ESTADOS,
    })


def leer_carrito(formulario):
    try:
        repuestos = json.loads(
            formulario.cleaned_data.get('repuestos_data') or '[]'
        )
    except (json.JSONDecodeError, TypeError):
        raise ValueError('Los datos del carrito no son válidos.')

    if not isinstance(repuestos, list):
        raise ValueError('Los datos del carrito no son válidos.')

    cantidades = {}

    try:
        for item in repuestos:
            identificador = int(item['id'])
            cantidad = int(item['cantidad'])

            if cantidad < 1:
                raise ValueError()

            if identificador in cantidades:
                raise ValueError()

            cantidades[identificador] = cantidad

    except (ValueError, TypeError, KeyError):
        raise ValueError(
            'Revisa los repuestos y las cantidades seleccionadas.'
        )

    return cantidades


def guardar_pedido(formulario, pedido=None):
    cantidades = leer_carrito(formulario)

    with transaction.atomic():

        # Si el pedido anterior estaba recibido,
        # primero revertimos las cantidades de su inventario.
        if pedido and pedido.estado == 'Recibido':

            detalles_anteriores = list(
                DetallePedido.objects.filter(pedido=pedido)
            )

            for detalle in detalles_anteriores:
                repuesto = Repuesto.objects.select_for_update().get(
                    pk=detalle.repuesto_id
                )

                if repuesto.cantidad < detalle.cantidad:
                    raise ValueError(
                        f'No se puede modificar el pedido porque el stock '
                        f'de {repuesto.nombre_pieza} ya fue utilizado.'
                    )

                repuesto.cantidad -= detalle.cantidad
                repuesto.save(update_fields=['cantidad'])

        # Buscar y bloquear los repuestos seleccionados.
        repuestos = {
            repuesto.pk: repuesto
            for repuesto in Repuesto.objects.select_for_update().filter(
                pk__in=cantidades.keys()
            )
        }

        if len(repuestos) != len(cantidades):
            raise ValueError(
                'Uno o más repuestos seleccionados ya no existen.'
            )

        # Guardar el pedido.
        pedido = formulario.save(commit=False)
        pedido.save()

        # Reemplazar los detalles anteriores.
        DetallePedido.objects.filter(pedido=pedido).delete()

        for identificador, cantidad in cantidades.items():

            repuesto = repuestos[identificador]

            DetallePedido.objects.create(
                pedido=pedido,
                repuesto=repuesto,
                cantidad=cantidad
            )

            # Sumar al inventario solamente si el pedido
            # se encuentra en estado Recibido.
            if pedido.estado == 'Recibido':
                repuesto.cantidad += cantidad
                repuesto.save(update_fields=['cantidad'])

        return pedido


def datos_formulario(pedido=None, formulario=None):

    repuestos_disponibles = [
        {
            'id': repuesto.pk,
            'nombre': repuesto.nombre_pieza,
            'costo': repuesto.costo,
            'stock': repuesto.cantidad,
        }
        for repuesto in Repuesto.objects.all().order_by('nombre_pieza')
    ]

    carrito_repuestos = []

    if formulario and formulario.is_bound:

        try:
            carrito_repuestos = json.loads(
                formulario.data.get('repuestos_data') or '[]'
            )
        except (json.JSONDecodeError, TypeError):
            pass

    elif pedido and pedido.pk:

        carrito_repuestos = [
            {
                'id': detalle.repuesto_id,
                'nombre': detalle.repuesto.nombre_pieza,
                'costo': detalle.repuesto.costo,
                'cantidad': detalle.cantidad,
            }
            for detalle in pedido.detalles.select_related('repuesto')
        ]

    return {
        'repuestos_disponibles': repuestos_disponibles,
        'carrito_repuestos': carrito_repuestos,
    }


def registrar_pedido(request):

    if request.method == 'POST':

        formulario = PedidoForm(request.POST)

        if formulario.is_valid():

            try:
                guardar_pedido(formulario)

                messages.success(
                    request,
                    'Pedido registrado con éxito.'
                )

                return redirect('lista_pedidos')

            except ValueError as error:
                formulario.add_error(None, str(error))

    else:
        formulario = PedidoForm()

    contexto = datos_formulario(formulario=formulario)

    return render(request, 'pedidos/registrar_pedido.html', {
        'formulario': formulario,
        **contexto,
    })


def editar_pedido(request, pk):

    pedido = get_object_or_404(Pedido, pk=pk)

    if request.method == 'POST':

        formulario = PedidoForm(
            request.POST,
            instance=pedido
        )

        if formulario.is_valid():

            try:
                guardar_pedido(formulario, pedido)

                messages.success(
                    request,
                    'Modificación exitosa.'
                )

                return redirect('lista_pedidos')

            except ValueError as error:
                formulario.add_error(None, str(error))

    else:
        formulario = PedidoForm(instance=pedido)

    contexto = datos_formulario(
        pedido=pedido,
        formulario=formulario if request.method == 'POST' else None
    )

    return render(request, 'pedidos/registrar_pedido.html', {
        'formulario': formulario,
        'pedido': pedido,
        **contexto,
    })


def eliminar_pedido(request, pk):

    pedido = get_object_or_404(Pedido, pk=pk)

    if request.method == 'POST':

        try:
            with transaction.atomic():

                # Si el pedido fue recibido, revertir su stock.
                if pedido.estado == 'Recibido':

                    detalles = list(
                        DetallePedido.objects.filter(pedido=pedido)
                    )

                    for detalle in detalles:

                        repuesto = Repuesto.objects.select_for_update().get(
                            pk=detalle.repuesto_id
                        )

                        if repuesto.cantidad < detalle.cantidad:
                            raise ValueError(
                                f'No se puede eliminar el pedido porque '
                                f'el stock de {repuesto.nombre_pieza} '
                                f'ya fue utilizado.'
                            )

                        repuesto.cantidad -= detalle.cantidad
                        repuesto.save(update_fields=['cantidad'])

                pedido.delete()

            messages.success(
                request,
                'Pedido eliminado con éxito.'
            )

        except ValueError as error:
            messages.error(request, str(error))

    return redirect('lista_pedidos')
