# core/views.py
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from .models import Estado, Accion
from .serializers import UsuarioSerializer, EstadoSerializer, AccionSerializer
from .game_logic import GameEngine

Usuario = get_user_model()


# ============================================================
# ENDPOINT 1: REGISTRO DE USUARIO
# ============================================================
@api_view(['POST'])
@permission_classes([AllowAny])
def registrar_usuario(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        Estado.objects.create(usuario=user)
        
        # Crear acciones base si no existen
        acciones_base = [
            {"nombre": "Explorar la jungla", "tipo": "explorar", "impacto_base": -5},
            {"nombre": "Recolectar frutas", "tipo": "recolectar", "impacto_base": -10},
            {"nombre": "Construir refugio", "tipo": "construir", "impacto_base": 5},
            {"nombre": "Descansar en la playa", "tipo": "descansar", "impacto_base": 15},
        ]
        for accion_data in acciones_base:
            Accion.objects.get_or_create(**accion_data)
        
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'user': serializer.data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================================
# ENDPOINT 2: LOGIN DE USUARIO
# ============================================================
@api_view(['POST'])
@permission_classes([AllowAny])
def login_usuario(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username})
    return Response({'error': 'Credenciales invalidas'}, status=status.HTTP_401_UNAUTHORIZED)


# ============================================================
# ENDPOINT 3: CONSULTAR ESTADO DEL USUARIO
# ============================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ver_estado(request):
    estado = request.user.estado
    serializer = EstadoSerializer(estado)
    return Response(serializer.data)


# ============================================================
# ENDPOINT 4: EJECUTAR ACCIÓN (EL MÁS IMPORTANTE)
# ============================================================
class EjecutarAccionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, accion_id):
        usuario = request.user
        estado = get_object_or_404(Estado, usuario=usuario)
        
        # Verificar si el jugador está vivo
        if not estado.esta_vivo:
            return Response({
                "error": "Tu personaje ha muerto",
                "dias_sobrevividos": usuario.dias_sobrevividos
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Obtener la acción
        accion = get_object_or_404(Accion, id=accion_id)
        
        # Ejecutar la lógica del juego
        resultado = GameEngine.ejecutar_accion(estado, accion)
        
        return Response(resultado, status=status.HTTP_200_OK)


# ============================================================
# ENDPOINT 5: LISTAR ACCIONES DISPONIBLES
# ============================================================
class AccionesDisponiblesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        acciones = Accion.objects.all()
        serializer = AccionSerializer(acciones, many=True)
        return Response(serializer.data)


# ============================================================
# ENDPOINT 6: RANKING DE JUGADORES
# ============================================================
class RankingView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        # Solo mostrar jugadores que ya murieron
        usuarios_muertos = Usuario.objects.filter(
            estado__esta_vivo=False
        ).order_by('-dias_sobrevividos')[:10]
        
        data = [
            {
                "username": u.username,
                "dias_sobrevividos": u.dias_sobrevividos
            }
            for u in usuarios_muertos
        ]
        
        return Response(data)