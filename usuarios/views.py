from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def iniciar_sesion(request):

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