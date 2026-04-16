from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registrar_usuario, name='register'),
    path('login/', views.login_usuario, name='login'),
    path('estado/', views.ver_estado, name='estado'),
]
