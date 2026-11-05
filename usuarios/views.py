
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST


def iniciar_sesion(request):
    # Si ya inició sesión, ir directamente al inicio.
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contraseña = request.POST.get('contraseña')

        usuario_autenticado = authenticate(
            request,
            username=usuario,
            password=contraseña
        )

        if usuario_autenticado is not None:
            login(request, usuario_autenticado)
            return redirect('home')

        return render(request, 'usuarios/login.html', {
            'error': 'Usuario o contraseña incorrectos.'
        })

    return render(request, 'usuarios/login.html')


@login_required
@require_POST
def cerrar_sesion(request):
    logout(request)
    return redirect('login')
