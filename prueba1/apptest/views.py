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
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
import requests
from django.conf import settings
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

@login_required
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


class UsuarioDetailView(APIView):
    authentication_classes = []  # Ya no requerimos autenticación por sesión/token automática

    def post(self, request):
        token_key = request.data.get('token')  # Ahora tomamos el token del cuerpo

        if not token_key:
            return Response({"detail": "Token no proporcionado."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return Response({"detail": "Token inválido."}, status=status.HTTP_400_BAD_REQUEST)

        usuario = token.user

        # Devolver los datos del usuario asociado al token
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)

class ObtainTokenView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'detail': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate the user using email and password
        user = authenticate(request, email=email, password=password)

        if user is None:
            raise AuthenticationFailed('Invalid email or password.')

        # Retrieve or create the token for the user
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key  # Return the existing or newly created token
        })
    
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

def verificar_juego(request):
    if request.method == "GET":
        nombre_usuario = request.GET.get('nombre_usuario')  # Obtener el nombre de usuario desde la URL
        if nombre_usuario:
            try:
                # Hacer la solicitud para obtener el Steam ID desde el nombre de usuario
                vanity_url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={settings.STEAM_API_KEY}&vanityurl={nombre_usuario}"
                response = requests.get(vanity_url)
                data = response.json()

                print(f"Nombre de usuario recibido: {nombre_usuario}")
                print(f"URL consultada para Steam ID: {vanity_url}")
                print(f"Respuesta API de VanityURL: {data}")  # Para ver la respuesta completa

                if data['response']['success'] == 1:
                    steam_id = data['response']['steamid']
                    print(f"Steam ID encontrado: {steam_id}")

                    # Verificamos si tiene *The Forest* en su biblioteca
                    juegos_url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={settings.STEAM_API_KEY}&steamid={steam_id}&include_appinfo=true&format=json"
                    juegos_response = requests.get(juegos_url)
                    juegos_data = juegos_response.json()

                    print(f"URL consultada para juegos: {juegos_url}")
                    print(f"Respuesta API de juegos: {juegos_data}")  # Para ver los juegos que tiene el usuario

                    tiene_the_forest = False
                    for juego in juegos_data['response'].get('games', []):
                        print(f"Juego encontrado: {juego.get('name', 'Sin nombre')} - AppID: {juego['appid']}")
                        if juego['appid'] == 242760:  # El AppID de *The Forest* es 242760
                            tiene_the_forest = True
                            print("¡The Forest está en la biblioteca del usuario!")
                            break

                    return render(request, 'micuentatf.html', {
                        'tiene_the_forest': tiene_the_forest,
                        'nombre_usuario': nombre_usuario,
                        'usuario': request.user
                    })

                else:
                    print(f"Error: Steam no pudo resolver el usuario '{nombre_usuario}'.")
                    print(f"Mensaje de Steam: {data['response'].get('message', 'Sin mensaje')}")
                    messages.error(request, 'Usuario no encontrado en Steam')
                    return render(request, 'micuentatf.html', {'usuario': request.user})

            except requests.exceptions.RequestException as e:
                print(f"Excepción al conectarse a Steam: {e}")
                messages.error(request, 'Hubo un problema al conectar con Steam, intente más tarde.')
                return render(request, 'micuentatf.html', {'usuario': request.user})

        else:
            print("No se ingresó ningún nombre de usuario.")
            messages.error(request, 'Debe ingresar un nombre de usuario de Steam')
            return render(request, 'micuentatf.html', {'usuario': request.user})

    return render(request, 'micuentatf.html', {'usuario': request.user})    