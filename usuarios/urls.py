from django.urls import path
from . import views


app_name = 'usuarios'

urlpatterns = [
    path('lista/', views.UsuariosList.as_view(), name='lista'),
    path('eliminar/<int:pk>', views.UsuarioEliminar.as_view(), name='eliminar'),
    path('editar/<int:pk>', views.UsuarioActualizar.as_view(), name='editar'),
    path('nuevo/', views.NuevoUsuario.as_view(), name='nuevo'),
    path('municipios/', views.obtiene_municipios, name='municipios'),
    path('ver/<int:pk>', views.UsuarioDetalle.as_view(), name='ver'),
    path('login/', views.LoginUsuario.as_view(), name='login'),
    path('signup/', views.SingupUsuario.as_view(), name='signup'),
    path('activar/<slug:uid64>/<slug:token>', views.ActivarCuenta.as_view(), name='activar'),
]
