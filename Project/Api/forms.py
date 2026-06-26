from django import forms
from .models import Reserva, Partido, Cancha, Estadio

class EstadioForm(forms.ModelForm):
    class Meta:
        model = Estadio
        fields = ['nombre', 'ciudad', 'pais', 'capacidad']

class CanchaForm(forms.ModelForm):
    class Meta:
        model = Cancha
        fields = ['estadio', 'numero', 'tipo', 'superficie', 'estado', 'largo', 'ancho']
        widgets = {
            'largo': forms.NumberInput(attrs={'step': '0.01'}),
            'ancho': forms.NumberInput(attrs={'step': '0.01'}),
        }

class PartidoForm(forms.ModelForm):
    class Meta:
        model = Partido
        fields = ['cancha', 'equipo_local', 'equipo_visitante', 'fecha', 'fase', 'arbitro',
                  'goles_local', 'goles_visitante']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['equipo', 'fecha_inicio', 'duracion_horas', 'motivo']
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'motivo': forms.Textarea(attrs={'rows': 3}),
        }