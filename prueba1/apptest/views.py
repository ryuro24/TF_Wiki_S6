from django.shortcuts import render, redirect
from apptest.forms import RegistroUsuarioForm, LoginForm, EditarUsernameForm, CambiarContrasenaForm
from apptest.models import Rol,Usuario
from django.contrib import messages
from allauth.socialaccount.providers.google.views import OAuth2LoginView
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from .serializers import UsuarioSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from django.http import Http404
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required
# Create your views here.

def custom_google_login(request):
    # Use the default Google OAuth2 login URL to redirect the user
    return redirect(OAuth2LoginView.as_view())

def inicio(request):
    return render(request, 'menuprincipal_wiki.html')

@login_required
def forowiki(request):
    if not request.user.is_authenticated:
        return redirect('inicio_sesion_wiki')  # Redirect to 'inicio_sesion_wiki' if not logged in
    
    return render(request, 'forowiki.html', {'usuario_email': request.user.email})

def registrarse_wiki(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)

            # Busca el rol "usuario" y se lo asigna
            try:
                rol_usuario = Rol.objects.get(nombre__iexact="usuario")
                usuario.rol = rol_usuario
            except Rol.DoesNotExist:
                # Si no existe, podrías crear uno o lanzar error
                rol_usuario = Rol.objects.create(nombre="usuario")
                usuario.rol = rol_usuario

            usuario.save()
            return redirect('inicio')  # O a donde quieras redirigir
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registrarse_wiki.html', {'form': form})

def inicio_sesion_wiki(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            password = form.cleaned_data['password']

            # Usamos el sistema de autenticación de Django
            usuario = authenticate(request, email=email, password=password)

            if usuario is not None:
                login(request, usuario)  # Inicia sesión usando el sistema de Django
                return redirect('inicio')
            else:
                form.add_error(None, 'Correo o contraseña incorrectos.')  # Error general

    else:
        form = LoginForm()

    return render(request, 'inicio_sesion_wiki.html', {
        'form': form
    })

def micuentatf(request):
    usuario = request.user
    username_form = EditarUsernameForm(instance=usuario)
    password_form = CambiarContrasenaForm()

    if request.method == 'POST':
        if 'edit_username' in request.POST:
            username_form = EditarUsernameForm(request.POST, instance=usuario)
            if username_form.is_valid():
                username_form.save()
                messages.success(request, 'Nombre de usuario actualizado.')
                return redirect('micuentatf')

        elif 'change_password' in request.POST:
            password_form = CambiarContrasenaForm(request.POST)
            if password_form.is_valid():
                new_password = password_form.cleaned_data['password']
                usuario.set_password(new_password)
                usuario.save()

                # Re-authenticate the user with the proper backend
                login(request, usuario, backend='django.contrib.auth.backends.ModelBackend')

                messages.success(request, 'Contraseña actualizada.')
                return redirect('micuentatf')

    return render(request, 'micuentatf.html', {
        'usuario': usuario,
        'username_form': username_form,
        'password_form': password_form,
    })

def Animales(request):
    return render(request, 'Animales.html')

def lugarestf(request):
    return render(request, 'Lugarestf.html')

def Enemigos(request):
    return render(request, 'Enemigos.html')

def Construcciones(request):
    return render(request, 'Construcciones.html')

def Flora(request):
    return render(request, 'Flora.html')

def Armas(request):
    return render(request, 'Armas.html')

def Consumibles(request):
    return render(request, 'Consumibles.html')

def historia(request):
    return render(request, 'historia.html')

def Logros(request):
    return render(request, 'Logros.html')

def cerrar_sesion(request):
    logout(request)  # Esto elimina toda la sesión y desconecta al usuario
    return redirect('inicio')

def recuperarcontra(request):
    return render(request, 'recuperarcontra.html')


class UsuarioDetailView(generics.RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_object(self):
        # Retrieve the user by email instead of id (pk)
        email = self.kwargs.get('email')
        try:
            usuario = Usuario.objects.get(email=email)
            return usuario
        except Usuario.DoesNotExist:
            raise Http404("Usuario no encontrado")

    def get(self, request, *args, **kwargs):
        usuario = self.get_object()  # Now it gets the user by email
        serializer = self.get_serializer(usuario)
        return Response(serializer.data)
    

def recuperar_contra(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            context['error'] = 'Las contraseñas no coinciden.'
        else:
            try:
                usuario = Usuario.objects.get(email=email)
                usuario.set_password(password1)
                usuario.save()
                context['success'] = 'Contraseña actualizada exitosamente.'
            except Usuario.DoesNotExist:
                context['error'] = 'El email no está registrado.'

    return render(request, 'recuperarcontra.html', context)
    