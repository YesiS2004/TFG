
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_servicios, name='lista_servicios'),
    path(
        'registrar/',
        views.registrar_servicio,
        name='registrar_servicio'
    ),
    path(
        '<int:pk>/editar/',
        views.editar_servicio,
        name='editar_servicio'
    ),
    path(
        '<int:pk>/eliminar/',
        views.eliminar_servicio,
        name='eliminar_servicio'
    ),
]
