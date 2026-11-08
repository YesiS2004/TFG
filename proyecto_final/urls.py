from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('usuarios.urls')),
    path('', include('home.urls')),
    path('clientes/', include('clientes.urls')),
    path('proveedores/', include('proveedores.urls')),
    path('servicios/', include('servicios.urls')),
    path('caracteristicas-vehiculos/', include('caracteristicas_vehiculos.urls')),
    path('repuestos/', include('repuestos.urls')),
    path('vehiculos/', include('vehiculos.urls')),
    path('reparaciones/', include('reparaciones.urls')),
    path('turnos/', include('turnos.urls')),
    path('pedidos/', include('pedidos.urls')),
]