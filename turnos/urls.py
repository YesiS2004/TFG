from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_turnos, name='lista_turnos'),
    path('registrar/', views.registrar_turno, name='registrar_turno'),
    path('editar/<int:pk>/', views.editar_turno, name='editar_turno'),
    path('eliminar/<int:pk>/', views.eliminar_turno, name='eliminar_turno'),
]