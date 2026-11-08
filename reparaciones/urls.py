from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_reparaciones, name='lista_reparaciones'),

    path(
        'registrar/',
        views.registrar_reparacion,
        name='registrar_reparacion'
    ),

    path(
        'editar/<int:pk>/',
        views.editar_reparacion,
        name='editar_reparacion'
    ),

    path(
        'eliminar/<int:pk>/',
        views.eliminar_reparacion,
        name='eliminar_reparacion'
    ),
]