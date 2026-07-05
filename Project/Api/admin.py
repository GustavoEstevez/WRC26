from django.contrib import admin
from .models import Estadio, Equipo, Jugador, Partido, Entrada, Perfil

@admin.register(Estadio)
class EstadioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ciudad', 'pais', 'capacidad']
    search_fields = ['nombre', 'ciudad']

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo_fifa', 'grupo']
    list_filter = ['grupo']

@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ['apellido', 'nombre', 'posicion', 'equipo']
    list_filter = ['posicion', 'equipo']

@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ['nombre_partido', 'fecha', 'fase', 'estadio']
    list_filter = ['fase']

@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'usuario', 'partido', 'categoria', 'cantidad', 'precio_total', 'estado']
    list_filter = ['estado', 'categoria']

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'rol']
    list_filter = ['rol']