
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_proveedores, name='lista_proveedores'),
    path(
        'registrar/',
        views.registrar_proveedor,
        name='registrar_proveedor'
    ),
    path(
        '<int:pk>/editar/',
        views.editar_proveedor,
        name='editar_proveedor'
    ),
    path(
        '<int:pk>/eliminar/',
        views.eliminar_proveedor,
        name='eliminar_proveedor'
    ),
]
