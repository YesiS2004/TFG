from django.urls import path
from .views import iniciar_sesion

urlpatterns = [
    path('login/', iniciar_sesion, name='login'),
]