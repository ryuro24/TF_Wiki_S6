"""
URL configuration for prueba1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apptest import views
from apptest.views import custom_google_login,UsuarioDetailView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(route='',view=views.inicio, name='inicio'),
    path('forowiki/', views.forowiki, name='forowiki'),
    path('registrarse_wiki/', views.registrarse_wiki, name='registrarse_wiki'),
    path('inicio_sesion_wiki/', views.inicio_sesion_wiki, name='inicio_sesion_wiki'),
    path('micuentatf/', views.micuentatf, name='micuentatf'),
    path('Animales/', views.Animales, name='Animales'),
    path('lugarestf/', views.lugarestf, name='lugarestf'),
    path('Enemigos/', views.Enemigos, name='Enemigos'),
    path('Construcciones/', views.Construcciones, name='Construcciones'),
    path('Flora/', views.Flora, name='Flora'),
    path('Armas/', views.Armas, name='Armas'),
    path('Consumibles/', views.Consumibles, name='Consumibles'),
    path('historia/', views.historia, name='historia'),
    path('Logros/', views.Logros, name='Logros'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('recuperar-contra/', views.recuperar_contra, name='recuperar_contra'),




    path('usuario/<str:email>/', views.UsuarioDetailView.as_view(), name='usuario-detail'),

    path('accounts/', include('allauth.urls')),
    path('accounts/google/login/', custom_google_login, name='google_login'),
    path('admin/', admin.site.urls),
]
