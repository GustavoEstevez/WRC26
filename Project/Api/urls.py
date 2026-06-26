from django.urls import path
from . import views

urlpatterns = [
    # Inicio
    path('', views.inicio, name='inicio'),

    # Estadios
    path('estadios/', views.lista_estadios, name='lista_estadios'),
    path('estadios/nuevo/', views.crear_estadio, name='crear_estadio'),
    path('estadios/<int:pk>/editar/', views.editar_estadio, name='editar_estadio'),
    path('estadios/<int:pk>/eliminar/', views.eliminar_estadio, name='eliminar_estadio'),

    # Canchas
    path('canchas/', views.lista_canchas, name='lista_canchas'),
    path('canchas/<int:pk>/', views.detalle_cancha, name='detalle_cancha'),
    path('canchas/nueva/', views.crear_cancha, name='crear_cancha'),
    path('canchas/<int:pk>/editar/', views.editar_cancha, name='editar_cancha'),
    path('canchas/<int:pk>/eliminar/', views.eliminar_cancha, name='eliminar_cancha'),

    # Partidos
    path('partidos/', views.lista_partidos, name='lista_partidos'),
    path('partidos/nuevo/', views.crear_partido, name='crear_partido'),
    path('partidos/<int:pk>/editar/', views.editar_partido, name='editar_partido'),
    path('partidos/<int:pk>/eliminar/', views.eliminar_partido, name='eliminar_partido'),

    # Reservas
    path('reservas/', views.lista_reservas, name='lista_reservas'),
    path('canchas/<int:cancha_id>/reservar/', views.crear_reserva, name='crear_reserva'),
    path('reservas/<int:pk>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),
]