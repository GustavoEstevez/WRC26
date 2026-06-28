from django.contrib import admin
from .models import Estadio, Cancha, Equipo, Jugador, Partido, Reserva, Perfil

@admin.register(Estadio)
class EstadioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ciudad', 'pais', 'capacidad']
    search_fields = ['nombre', 'ciudad', 'pais']

@admin.register(Cancha)
class CanchaAdmin(admin.ModelAdmin):
    list_display = ['numero', 'estadio', 'tipo', 'superficie', 'estado']
    list_filter = ['estado', 'tipo', 'superficie']

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo_fifa', 'pais', 'grupo']
    list_filter = ['grupo']

@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ['apellido', 'nombre', 'numero_camiseta', 'posicion', 'equipo']
    list_filter = ['posicion', 'equipo']

@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ['equipo_local', 'equipo_visitante', 'fecha', 'fase']
    list_filter = ['fase']

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['cancha', 'equipo', 'fecha_inicio', 'duracion_horas', 'estado']
    list_filter = ['estado']

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'rol']
    list_filter = ['rol']