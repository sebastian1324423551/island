# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('register/', views.registrar_usuario, name='register'),
    path('login/', views.login_usuario, name='login'),
    
    # Estado
    path('estado/', views.ver_estado, name='estado'),
    
    # Acciones
    path('acciones/', views.AccionesDisponiblesView.as_view(), name='acciones'),
    path('jugar/<int:accion_id>/', views.EjecutarAccionView.as_view(), name='jugar'),
    
    # Ranking
    path('ranking/', views.RankingView.as_view(), name='ranking'),
]