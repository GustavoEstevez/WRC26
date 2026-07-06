from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Estadio, Equipo, Partido, Entrada


class EstadioForm(forms.ModelForm):
    class Meta:
        model = Estadio
        fields = ['nombre', 'ciudad', 'pais', 'capacidad', 'imagen', 'latitud', 'longitud']


class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre', 'pais', 'codigo_fifa', 'grupo', 'entrenador']


class PartidoForm(forms.ModelForm):
    class Meta:
        model = Partido
        fields = ['estadio', 'equipo_local', 'equipo_visitante', 'descripcion',
                  'fecha', 'fase', 'arbitro', 'precio_general', 'precio_platea',
                  'precio_vip', 'entradas_disponibles']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class EntradaForm(forms.Form):
    categoria = forms.ChoiceField(
        choices=[('general', 'General'), ('platea', 'Platea'), ('vip', 'VIP')],
        widget=forms.RadioSelect,
        initial='general'
    )
    cantidad = forms.IntegerField(min_value=1, max_value=10, initial=1)


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']