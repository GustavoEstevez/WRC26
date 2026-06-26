from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Estadio, Cancha, Equipo, Partido, Reserva
from .forms import ReservaForm, PartidoForm, CanchaForm, EstadioForm

# ─── INICIO ───────────────────────────────────────────────
def inicio(request):
    estadios = Estadio.objects.all()
    partidos_proximos = Partido.objects.filter(
        goles_local__isnull=True
    ).order_by('fecha')[:5]
    return render(request, 'Api/inicio.html', {
        'estadios': estadios,
        'partidos_proximos': partidos_proximos,
    })

# ─── CANCHAS ──────────────────────────────────────────────
def lista_canchas(request):
    canchas = Cancha.objects.select_related('estadio').all()
    return render(request, 'Api/lista_canchas.html', {'canchas': canchas})

def detalle_cancha(request, pk):
    cancha = get_object_or_404(Cancha, pk=pk)
    reservas = cancha.reservas.filter(estado='confirmada')
    return render(request, 'Api/detalle_cancha.html', {
        'cancha': cancha,
        'reservas': reservas,
    })

def crear_cancha(request):
    form = CanchaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cancha creada correctamente.')
        return redirect('lista_canchas')
    return render(request, 'Api/form_cancha.html', {'form': form, 'titulo': 'Nueva Cancha'})

def editar_cancha(request, pk):
    cancha = get_object_or_404(Cancha, pk=pk)
    form = CanchaForm(request.POST or None, instance=cancha)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cancha actualizada.')
        return redirect('lista_canchas')
    return render(request, 'Api/form_cancha.html', {'form': form, 'titulo': 'Editar Cancha'})

def eliminar_cancha(request, pk):
    cancha = get_object_or_404(Cancha, pk=pk)
    if request.method == 'POST':
        cancha.delete()
        messages.success(request, 'Cancha eliminada.')
        return redirect('lista_canchas')
    return render(request, 'Api/confirmar_eliminar.html', {'objeto': cancha, 'tipo': 'cancha'})

# ─── ESTADIOS ─────────────────────────────────────────────
def lista_estadios(request):
    estadios = Estadio.objects.all()
    return render(request, 'Api/lista_estadios.html', {'estadios': estadios})

def crear_estadio(request):
    form = EstadioForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Estadio creado correctamente.')
        return redirect('lista_estadios')
    return render(request, 'Api/form_estadio.html', {'form': form, 'titulo': 'Nuevo Estadio'})

def editar_estadio(request, pk):
    estadio = get_object_or_404(Estadio, pk=pk)
    form = EstadioForm(request.POST or None, instance=estadio)
    if form.is_valid():
        form.save()
        messages.success(request, 'Estadio actualizado.')
        return redirect('lista_estadios')
    return render(request, 'Api/form_estadio.html', {'form': form, 'titulo': 'Editar Estadio'})

def eliminar_estadio(request, pk):
    estadio = get_object_or_404(Estadio, pk=pk)
    if request.method == 'POST':
        estadio.delete()
        messages.success(request, 'Estadio eliminado.')
        return redirect('lista_estadios')
    return render(request, 'Api/confirmar_eliminar.html', {'objeto': estadio, 'tipo': 'estadio'})

# ─── PARTIDOS ─────────────────────────────────────────────
def lista_partidos(request):
    partidos = Partido.objects.select_related(
        'cancha__estadio', 'equipo_local', 'equipo_visitante'
    ).all()
    return render(request, 'Api/lista_partidos.html', {'partidos': partidos})

def crear_partido(request):
    form = PartidoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Partido creado correctamente.')
        return redirect('lista_partidos')
    return render(request, 'Api/form_partido.html', {'form': form, 'titulo': 'Nuevo Partido'})

def editar_partido(request, pk):
    partido = get_object_or_404(Partido, pk=pk)
    form = PartidoForm(request.POST or None, instance=partido)
    if form.is_valid():
        form.save()
        messages.success(request, 'Partido actualizado.')
        return redirect('lista_partidos')
    return render(request, 'Api/form_partido.html', {'form': form, 'titulo': 'Editar Partido'})

def eliminar_partido(request, pk):
    partido = get_object_or_404(Partido, pk=pk)
    if request.method == 'POST':
        partido.delete()
        messages.success(request, 'Partido eliminado.')
        return redirect('lista_partidos')
    return render(request, 'Api/confirmar_eliminar.html', {'objeto': partido, 'tipo': 'partido'})

# ─── RESERVAS ─────────────────────────────────────────────
def lista_reservas(request):
    reservas = Reserva.objects.select_related('cancha__estadio', 'equipo').all()
    return render(request, 'Api/lista_reservas.html', {'reservas': reservas})

def crear_reserva(request, cancha_id):
    cancha = get_object_or_404(Cancha, pk=cancha_id)
    form = ReservaForm(request.POST or None)
    if form.is_valid():
        reserva = form.save(commit=False)
        reserva.cancha = cancha
        reserva.save()
        messages.success(request, 'Reserva creada correctamente.')
        return redirect('detalle_cancha', pk=cancha_id)
    return render(request, 'Api/form_reserva.html', {'form': form, 'cancha': cancha})

def cancelar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        reserva.estado = 'cancelada'
        reserva.save()
        messages.success(request, 'Reserva cancelada.')
        return redirect('lista_reservas')
    return render(request, 'Api/confirmar_eliminar.html', {'objeto': reserva, 'tipo': 'reserva'})