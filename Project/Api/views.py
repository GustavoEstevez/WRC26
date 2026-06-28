from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Estadio, Cancha, Equipo, Partido, Reserva
from .forms import ReservaForm, PartidoForm, CanchaForm, EstadioForm, EquipoForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from .forms import RegistroForm
from .models import Perfil

def solo_admin(view_func):
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'perfil') and request.user.perfil.rol == 'admin':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper

def error_403(request, exception):
    return render(request, 'canchas/403.html', status=403)

# ─── INICIO ───────────────────────────────────────────────
@login_required
def inicio(request):
    estadios = Estadio.objects.all()
    partidos_proximos = Partido.objects.filter(
        goles_local__isnull=True
    ).order_by('fecha')[:5]
    return render(request, 'canchas/inicio.html', {
        'estadios': estadios,
        'partidos_proximos': partidos_proximos,
    })

def registro(request):
    form = RegistroForm(request.POST or None)
    if form.is_valid():
        usuario = form.save()
        Perfil.objects.create(usuario=usuario, rol='operador')  # por defecto operador
        messages.success(request, 'Usuario creado correctamente. Ya podés iniciar sesión.')
        return redirect('login')
    return render(request, 'canchas/registro.html', {'form': form})

# ─── EQUIPOS ──────────────────────────────────────────────
@login_required
def lista_equipos(request):
    equipos = Equipo.objects.all()
    return render(request, 'canchas/lista_equipos.html', {'equipos': equipos})

@login_required
@solo_admin
def crear_equipo(request):
    form = EquipoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Equipo creado correctamente.')
        return redirect('lista_equipos')
    return render(request, 'canchas/form_equipo.html', {'form': form, 'titulo': 'Nuevo Equipo'})

@login_required
@solo_admin
def editar_equipo(request, pk):
    equipo = get_object_or_404(Equipo, pk=pk)
    form = EquipoForm(request.POST or None, instance=equipo)
    if form.is_valid():
        form.save()
        messages.success(request, 'Equipo actualizado.')
        return redirect('lista_equipos')
    return render(request, 'canchas/form_equipo.html', {'form': form, 'titulo': 'Editar Equipo'})

@login_required
@solo_admin
def eliminar_equipo(request, pk):
    equipo = get_object_or_404(Equipo, pk=pk)
    if request.method == 'POST':
        equipo.delete()
        messages.success(request, 'Equipo eliminado.')
        return redirect('lista_equipos')
    return render(request, 'canchas/confirmar_eliminar.html', {'objeto': equipo, 'tipo': 'equipo'})

# ─── CANCHAS ──────────────────────────────────────────────
@login_required
def lista_canchas(request):
    canchas = Cancha.objects.select_related('estadio').all()
    return render(request, 'canchas/lista_canchas.html', {'canchas': canchas})

def detalle_cancha(request, pk):
    cancha = get_object_or_404(Cancha, pk=pk)
    reservas = cancha.reservas.filter(estado='confirmada')
    return render(request, 'canchas/detalle_cancha.html', {
        'cancha': cancha,
        'reservas': reservas,
    })

@login_required
@solo_admin
def crear_cancha(request):
    form = CanchaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cancha creada correctamente.')
        return redirect('lista_canchas')
    return render(request, 'canchas/form_cancha.html', {'form': form, 'titulo': 'Nueva Cancha'})

@login_required
@solo_admin
def editar_cancha(request, pk):
    cancha = get_object_or_404(Cancha, pk=pk)
    form = CanchaForm(request.POST or None, instance=cancha)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cancha actualizada.')
        return redirect('lista_canchas')
    return render(request, 'canchas/form_cancha.html', {'form': form, 'titulo': 'Editar Cancha'})
    
@login_required
@solo_admin
def eliminar_cancha(request, pk):
    cancha = get_object_or_404(Cancha, pk=pk)
    if request.method == 'POST':
        cancha.delete()
        messages.success(request, 'Cancha eliminada.')
        return redirect('lista_canchas')
    return render(request, 'canchas/confirmar_eliminar.html', {'objeto': cancha, 'tipo': 'cancha'})

# ─── ESTADIOS ─────────────────────────────────────────────
@login_required 
def lista_estadios(request):
    estadios = Estadio.objects.all()
    return render(request, 'canchas/lista_estadios.html', {'estadios': estadios})
    
@login_required
@solo_admin
def crear_estadio(request):
    form = EstadioForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Estadio creado correctamente.')
        return redirect('lista_estadios')
    return render(request, 'canchas/form_estadio.html', {'form': form, 'titulo': 'Nuevo Estadio'})

@login_required
@solo_admin
def editar_estadio(request, pk):
    estadio = get_object_or_404(Estadio, pk=pk)
    form = EstadioForm(request.POST or None, instance=estadio)
    if form.is_valid():
        form.save()
        messages.success(request, 'Estadio actualizado.')
        return redirect('lista_estadios')
    return render(request, 'canchas/form_estadio.html', {'form': form, 'titulo': 'Editar Estadio'})

@login_required
@solo_admin
def eliminar_estadio(request, pk):
    estadio = get_object_or_404(Estadio, pk=pk)
    if request.method == 'POST':
        estadio.delete()
        messages.success(request, 'Estadio eliminado.')
        return redirect('lista_estadios')
    return render(request, 'canchas/confirmar_eliminar.html', {'objeto': estadio, 'tipo': 'estadio'})

# ─── PARTIDOS ─────────────────────────────────────────────
@login_required
def lista_partidos(request):
    partidos = Partido.objects.select_related(
        'cancha__estadio', 'equipo_local', 'equipo_visitante'
    ).all()
    return render(request, 'canchas/lista_partidos.html', {'partidos': partidos})

@login_required
@solo_admin
def crear_partido(request):
    form = PartidoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Partido creado correctamente.')
        return redirect('lista_partidos')
    return render(request, 'canchas/form_partido.html', {'form': form, 'titulo': 'Nuevo Partido'})

@login_required
@solo_admin
def editar_partido(request, pk):
    partido = get_object_or_404(Partido, pk=pk)
    form = PartidoForm(request.POST or None, instance=partido)
    if form.is_valid():
        form.save()
        messages.success(request, 'Partido actualizado.')
        return redirect('lista_partidos')
    return render(request, 'canchas/form_partido.html', {'form': form, 'titulo': 'Editar Partido'})

@login_required
@solo_admin
def eliminar_partido(request, pk):
    partido = get_object_or_404(Partido, pk=pk)
    if request.method == 'POST':
        partido.delete()
        messages.success(request, 'Partido eliminado.')
        return redirect('lista_partidos')
    return render(request, 'canchas/confirmar_eliminar.html', {'objeto': partido, 'tipo': 'partido'})

# ─── RESERVAS ─────────────────────────────────────────────
@login_required
def lista_reservas(request):
    reservas = Reserva.objects.select_related('cancha__estadio', 'equipo').all()
    return render(request, 'canchas/lista_reservas.html', {'reservas': reservas})

@login_required
def crear_reserva(request, cancha_id):
    cancha = get_object_or_404(Cancha, pk=cancha_id)
    form = ReservaForm(request.POST or None)
    if form.is_valid():
        reserva = form.save(commit=False)
        reserva.cancha = cancha
        reserva.save()
        messages.success(request, 'Reserva creada correctamente.')
        return redirect('detalle_cancha', pk=cancha_id)
    return render(request, 'canchas/form_reserva.html', {'form': form, 'cancha': cancha})

@login_required
def cancelar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        reserva.estado = 'cancelada'
        reserva.save()
        messages.success(request, 'Reserva cancelada.')
        return redirect('lista_reservas')
    return render(request, 'canchas/confirmar_eliminar.html', {'objeto': reserva, 'tipo': 'reserva'})


import json

@login_required
def mapa_estadios(request):
    estadios = Estadio.objects.filter(
        latitud__isnull=False,
        longitud__isnull=False
    )
    # Convertir a lista para pasarla al template como JSON
    estadios_json = json.dumps([
        {
            'nombre': e.nombre,
            'ciudad': e.ciudad,
            'pais': e.pais,
            'capacidad': e.capacidad,
            'lat': float(e.latitud),
            'lng': float(e.longitud),
        }
        for e in estadios
    ])
    return render(request, 'canchas/mapa_estadios.html', {
        'estadios_json': estadios_json,
        'estadios': estadios,
    })

def error_403(request, exception):
    return render(request, 'canchas/403.html', status=403)