from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Estado, Accion

Usuario = get_user_model()

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'password', 'fecha_registro']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user

class EstadoSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='usuario.username')
    
    class Meta:
        model = Estado
        fields = ['id', 'username', 'dia_actual', 'hambre', 'salud', 'esta_vivo']

class AccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accion
        fields = '__all__'
