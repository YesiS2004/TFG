
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_repuestos, name='lista_repuestos'),
    path('registrar/', views.registrar_repuesto, name='registrar_repuesto'),
    path('<int:pk>/editar/', views.editar_repuesto, name='editar_repuesto'),
    path('<int:pk>/eliminar/', views.eliminar_repuesto, name='eliminar_repuesto'),
]
