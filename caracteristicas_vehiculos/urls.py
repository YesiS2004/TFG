from django.urls import path, include
from . import views

urlpatterns = [
    path('marcas/', views.lista_marcas, name='lista_marcas'),
    path('marcas/registrar/', views.registrar_marca, name='registrar_marca'),
    path('marcas/<int:pk>/editar/', views.editar_marca, name='editar_marca'),

    path('modelos/', views.lista_modelos, name='lista_modelos'),
    path('modelos/registrar/', views.registrar_modelo, name='registrar_modelo'),
    path('modelos/<int:pk>/editar/', views.editar_modelo, name='editar_modelo'),

]
