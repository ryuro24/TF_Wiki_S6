from django.contrib import admin

# Register your models here.
from .models import Usuario, Rol
admin.site.register(Usuario)
admin.site.register(Rol)