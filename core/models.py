from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Usuario(AbstractUser):
    fecha_registro = models.DateTimeField(auto_now_add=True)
    dias_sobrevividos = models.IntegerField(default=0)
    
    def __str__(self):
        return self.username

class Estado(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='estado')
    dia_actual = models.IntegerField(default=1)
    hambre = models.IntegerField(default=100)
    salud = models.IntegerField(default=100)
    esta_vivo = models.BooleanField(default=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.usuario.username} - Día {self.dia_actual}"
    
    def verificar_muerte(self):
        if self.hambre <= 0 or self.salud <= 0:
            self.esta_vivo = False
            self.save()
            return True
        return False

class Accion(models.Model):
    TIPOS_ACCION = [
        ('explorar', 'Explorar'),
        ('recolectar', 'Recolectar'),
        ('construir', 'Construir'),
        ('descansar', 'Descansar'),
    ]
    
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS_ACCION)
    impacto_base = models.IntegerField()
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.tipo})"
