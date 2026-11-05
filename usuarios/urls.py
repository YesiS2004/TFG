
from django.urls import path
from .views import iniciar_sesion, cerrar_sesion

urlpatterns = [
    path('', iniciar_sesion, name='login'),
    path('logout/', cerrar_sesion, name='logout'),
]
