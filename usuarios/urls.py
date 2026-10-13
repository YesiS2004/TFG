from django.urls import path
from .views import iniciar_sesion

urlpatterns = [
    path('', iniciar_sesion, name='login'),
]