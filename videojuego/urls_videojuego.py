from django.urls import path
from . import views


app_name = 'videojuego'

urlpatterns = [
    path('lista/', views.VideojuegoList.as_view(), name='lista'),
    path('nuevo/', views.VideojuegoCrear.as_view(), name='nuevo'),
    path('eliminar/<int:pk>', views.VideojuegoEliminar.as_view(), name='eliminar'),
    path('editar/<int:pk>', views.VideojuegoActualizar.as_view(), name='editar'),
    path('ver/<int:pk>', views.VideojuegoDetalle.as_view(), name='ver'),

    path('grafica/', views.Grafica.as_view(), name='grafica_videojuegos'),
    path('pdf/', views.VideojuegoPDF.as_view(), name='videojuego_pdf'),
    path('pdf-detalle/<int:pk>', views.VideojuegoPDFDetalle.as_view(), name='pdf_detalle'),

    path('comprar/', views.comprar,name='comprar'),
    path('resumen-compra/',views.resumen_compra,name='resumen'),
]
