from django.urls import path
from . import views

urlpatterns = [
    # Inicio
    path('', views.inicio, name='inicio'),

    # Auth
    path('registro/', views.registro, name='registro'),

    # Estadios
    path('estadios/', views.lista_estadios, name='lista_estadios'),
    path('estadios/nuevo/', views.crear_estadio, name='crear_estadio'),
    path('estadios/<int:pk>/editar/', views.editar_estadio, name='editar_estadio'),
    path('estadios/<int:pk>/eliminar/', views.eliminar_estadio, name='eliminar_estadio'),
    path('mapa/', views.mapa_estadios, name='mapa_estadios'),

    # Equipos
    path('equipos/', views.lista_equipos, name='lista_equipos'),
    path('equipos/nuevo/', views.crear_equipo, name='crear_equipo'),
    path('equipos/<int:pk>/editar/', views.editar_equipo, name='editar_equipo'),
    path('equipos/<int:pk>/eliminar/', views.eliminar_equipo, name='eliminar_equipo'),
    path('equipos/<int:pk>/', views.detalle_equipo, name='detalle_equipo'),

    # Partidos
    path('partidos/', views.lista_partidos, name='lista_partidos'),
    path('partidos/<int:pk>/', views.detalle_partido, name='detalle_partido'),
    path('partidos/nuevo/', views.crear_partido, name='crear_partido'),
    path('partidos/<int:pk>/editar/', views.editar_partido, name='editar_partido'),
    path('partidos/<int:pk>/eliminar/', views.eliminar_partido, name='eliminar_partido'),

    # Carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:pk>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/eliminar/<str:key>/', views.eliminar_carrito, name='eliminar_carrito'),  
    path('carrito/confirmar/', views.confirmar_compra, name='confirmar_compra'),
    path('carrito/procesar/', views.procesar_pago, name='procesar_pago'),
    path('carrito/exitoso/', views.compra_exitosa, name='compra_exitosa'),

    # Mis entradas
    path('mis-entradas/', views.mis_entradas, name='mis_entradas'),
]