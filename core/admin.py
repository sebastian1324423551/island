from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Estado, Accion

admin.site.register(Usuario, UserAdmin)
admin.site.register(Estado)
admin.site.register(Accion)
