from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.db import models
from .models import Estadio, Equipo, Partido, Entrada, Perfil
from .forms import EstadioForm, EquipoForm, PartidoForm, EntradaForm, RegistroForm
import json


# ─── DECORADOR ADMIN ──────────────────────────────────────
def solo_admin(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            if request.user.perfil.rol == 'admin':
                return view_func(request, *args, **kwargs)
        except:
            pass
        raise PermissionDenied
    return wrapper


def error_403(request, exception=None):
    return render(request, 'canchas/403.html', status=403)


# ─── INICIO ───────────────────────────────────────────────
@login_required
def inicio(request):
    from datetime import datetime
    partidos_proximos = Partido.objects.filter(
        fecha__gt=timezone.now()
    ).select_related('estadio', 'equipo_local', 'equipo_visitante').order_by('fecha')[:6]
    partido_destacado = partidos_proximos.first()
    partido_final = Partido.objects.filter(fase='final').select_related('estadio', 'equipo_local', 'equipo_visitante').first()
    hoy = timezone.make_aware(datetime(2026, 7, 7))
    partidos_destacados = Partido.objects.filter(
        fecha__gte=hoy
    ).select_related('estadio', 'equipo_local', 'equipo_visitante').order_by('fecha')
    estadios = Estadio.objects.all()
    total_equipos = Equipo.objects.count()
    total_partidos = Partido.objects.count()
    return render(request, 'canchas/inicio.html', {
        'partidos_proximos': partidos_proximos,
        'partido_destacado': partido_destacado,
        'partido_final': partido_final,
        'partidos_destacados': partidos_destacados,
        'estadios': estadios,
        'total_equipos': total_equipos,
        'total_partidos': total_partidos,
    })


# ─── AUTH ─────────────────────────────────────────────────
def registro(request):
    form = RegistroForm(request.POST or None)
    if form.is_valid():
        usuario = form.save()
        Perfil.objects.create(usuario=usuario, rol='operador')
        messages.success(request, 'Cuenta creada. Ya podés iniciar sesión.')
        return redirect('login')
    return render(request, 'canchas/registro.html', {'form': form})


# ─── ESTADIOS ─────────────────────────────────────────────
@login_required
def lista_estadios(request):
    estadios = Estadio.objects.all()
    return render(request, 'canchas/lista_estadios.html', {'estadios': estadios})


@login_required
@solo_admin
def crear_estadio(request):
    form = EstadioForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Estadio creado.')
        return redirect('lista_estadios')
    return render(request, 'canchas/form_estadio.html', {'form': form, 'titulo': 'Nuevo Estadio'})


@login_required
@solo_admin
def editar_estadio(request, pk):
    estadio = get_object_or_404(Estadio, pk=pk)
    form = EstadioForm(request.POST or None, request.FILES or None, instance=estadio)
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
    return render(request, 'canchas/confirmar_eliminar.html', {'objeto': estadio})


@login_required
def mapa_estadios(request):
    estadios = Estadio.objects.filter(latitud__isnull=False, longitud__isnull=False)
    destacar_id = request.GET.get('destacar')
    try:
        destacar_id = int(destacar_id) if destacar_id else None
    except (ValueError, TypeError):
        destacar_id = None
    estadios_json = json.dumps([{
        'id': e.id,
        'nombre': e.nombre,
        'ciudad': e.ciudad,
        'pais': e.pais,
        'capacidad': e.capacidad,
        'imagen': e.imagen.url if e.imagen else '',
        'lat': float(e.latitud),
        'lng': float(e.longitud),
    } for e in estadios])
    return render(request, 'canchas/mapa_estadios.html', {
        'estadios_json': estadios_json,
        'estadios': estadios,
        'destacar_id': destacar_id,
    })


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
        messages.success(request, 'Equipo creado.')
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
    return render(request, 'canchas/confirmar_eliminar.html', {'objeto': equipo})


@login_required
def detalle_equipo(request, pk):
    equipo = get_object_or_404(Equipo, pk=pk)
    partidos = Partido.objects.filter(
        models.Q(equipo_local=equipo) | models.Q(equipo_visitante=equipo)
    ).select_related('estadio', 'equipo_local', 'equipo_visitante').order_by('fecha')
    return render(request, 'canchas/detalle_equipo.html', {
        'equipo': equipo,
        'partidos': partidos,
        'FASE_CHOICES': Partido.FASE_CHOICES,
    })


# ─── PARTIDOS ─────────────────────────────────────────────
@login_required
def lista_partidos(request):
    fase = request.GET.get('fase', '')
    equipo = request.GET.get('equipo', '')
    pais = request.GET.get('pais', '')
    ciudad = request.GET.get('ciudad', '')
    estadio_id = request.GET.get('estadio', '')

    partidos = Partido.objects.select_related('estadio', 'equipo_local', 'equipo_visitante')

    if fase:
        partidos = partidos.filter(fase=fase)
    if equipo:
        partidos = partidos.filter(
            models.Q(equipo_local_id=equipo) | models.Q(equipo_visitante_id=equipo)
        )
    if pais:
        partidos = partidos.filter(estadio__pais__icontains=pais)
    if ciudad:
        partidos = partidos.filter(estadio__ciudad__icontains=ciudad)
    if estadio_id:
        partidos = partidos.filter(estadio_id=estadio_id)

    estadios = Estadio.objects.all().order_by('pais', 'ciudad', 'nombre')
    paises = Estadio.objects.values_list('pais', flat=True).distinct().order_by('pais')
    ciudades = Estadio.objects.values_list('ciudad', flat=True).distinct().order_by('ciudad')
    equipos = Equipo.objects.all().order_by('nombre')
    return render(request, 'canchas/lista_partidos.html', {
        'partidos': partidos,
        'fase_actual': fase,
        'equipo_actual': equipo,
        'pais_actual': pais,
        'ciudad_actual': ciudad,
        'estadio_actual': estadio_id,
        'FASE_CHOICES': Partido.FASE_CHOICES,
        'equipos': equipos,
        'estadios': estadios,
        'paises': paises,
        'ciudades': ciudades,
    })


@login_required
def detalle_partido(request, pk):
    partido = get_object_or_404(Partido, pk=pk)
    form = EntradaForm()
    return render(request, 'canchas/detalle_partido.html', {
        'partido': partido,
        'form': form,
    })


@login_required
@solo_admin
def crear_partido(request):
    form = PartidoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Partido creado.')
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
    return render(request, 'canchas/confirmar_eliminar.html', {'objeto': partido})


# ─── CARRITO ──────────────────────────────────────────────
@login_required
def agregar_carrito(request, pk):
    partido = get_object_or_404(Partido, pk=pk)
    if request.method == 'POST':
        form = EntradaForm(request.POST)
        if form.is_valid():
            categoria = form.cleaned_data['categoria']
            cantidad = form.cleaned_data['cantidad']
            carrito = request.session.get('carrito', {})
            key = str(pk)
            if key in carrito:
                carrito[key]['cantidad'] += cantidad
            else:
                precios = {
                    'general': float(partido.precio_general),
                    'platea': float(partido.precio_platea),
                    'vip': float(partido.precio_vip),
                }
                carrito[key] = {
                    'partido_id': pk,
                    'partido_nombre': partido.nombre_partido(),
                    'partido_fecha': partido.fecha.strftime('%d/%m/%Y %H:%M'),
                    'categoria': categoria,
                    'cantidad': cantidad,
                    'precio_unitario': precios[categoria],
                }
            request.session['carrito'] = carrito
            messages.success(request, 'Entrada agregada al carrito.')
            return redirect('ver_carrito')
    return redirect('detalle_partido', pk=pk)


@login_required
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    total = 0
    partido_ids = []
    for key, item in carrito.items():
        subtotal = item['precio_unitario'] * item['cantidad']
        total += subtotal
        items.append({**item, 'subtotal': subtotal, 'key': key})
        partido_ids.append(item['partido_id'])
    partidos_qs = Partido.objects.filter(id__in=partido_ids).select_related(
        'estadio', 'equipo_local', 'equipo_visitante'
    )
    partidos_map = {p.id: p for p in partidos_qs}
    for item in items:
        item['partido_obj'] = partidos_map.get(item['partido_id'])
    return render(request, 'canchas/carrito.html', {
        'items': items,
        'total': total,
    })


@login_required
def eliminar_carrito(request, key):
    carrito = request.session.get('carrito', {})
    if key in carrito:
        del carrito[key]
        request.session['carrito'] = carrito
        messages.success(request, 'Entrada eliminada del carrito.')
    return redirect('ver_carrito')


@login_required
def confirmar_compra(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('lista_partidos')
    
    items = []
    total = 0
    for key, item in carrito.items():
        subtotal = item['precio_unitario'] * item['cantidad']
        total += subtotal
        items.append({**item, 'subtotal': subtotal, 'key': key})

    return render(request, 'canchas/pago.html', {
        'items': items,
        'total': total,
    })


@login_required
def procesar_pago(request):
    if request.method != 'POST':
        return redirect('ver_carrito')

    carrito = request.session.get('carrito', {})
    if not carrito:
        return redirect('lista_partidos')

    # Validaciones básicas del formulario
    metodo = request.POST.get('metodo_pago')
    
    if metodo == 'tarjeta':
        numero = request.POST.get('numero_tarjeta', '').replace(' ', '')
        nombre = request.POST.get('nombre_tarjeta', '')
        vencimiento = request.POST.get('vencimiento', '')
        cvv = request.POST.get('cvv', '')

        if len(numero) != 16 or not numero.isdigit():
            messages.error(request, 'El número de tarjeta debe tener 16 dígitos.')
            return redirect('confirmar_compra')
        if not nombre:
            messages.error(request, 'Ingresá el nombre del titular.')
            return redirect('confirmar_compra')
        if len(vencimiento) != 5:
            messages.error(request, 'Ingresá una fecha de vencimiento válida (MM/AA).')
            return redirect('confirmar_compra')
        if len(cvv) not in [3, 4]:
            messages.error(request, 'El CVV debe tener 3 o 4 dígitos.')
            return redirect('confirmar_compra')

    # Procesar la compra
    entradas_creadas = []
    for key, item in carrito.items():
        partido = get_object_or_404(Partido, pk=item['partido_id'])
        precios = {
            'general': partido.precio_general,
            'platea': partido.precio_platea,
            'vip': partido.precio_vip,
        }
        entrada = Entrada.objects.create(
            partido=partido,
            usuario=request.user,
            categoria=item['categoria'],
            cantidad=item['cantidad'],
            precio_unitario=precios[item['categoria']],
            estado='confirmada',
        )
        entradas_creadas.append(entrada)

    request.session['carrito'] = {}
    request.session['ultima_compra'] = [e.codigo for e in entradas_creadas]

    return redirect('compra_exitosa')


@login_required
def compra_exitosa(request):
    codigos = request.session.get('ultima_compra', [])
    entradas = Entrada.objects.filter(codigo__in=codigos).select_related('partido__estadio')
    return render(request, 'canchas/compra_exitosa.html', {'entradas': entradas})

# ─── MIS ENTRADAS ─────────────────────────────────────────
@login_required
def mis_entradas(request):
    entradas = Entrada.objects.filter(
        usuario=request.user,
        estado='confirmada'
    ).select_related('partido__estadio')

    proximas = []
    pasadas = []
    ahora = timezone.now()

    for e in entradas:
        if e.partido.fecha > ahora:
            proximas.append(e)
        else:
            pasadas.append(e)

    # Próximo partido más cercano
    proximo = proximas[0] if proximas else None

    return render(request, 'canchas/mis_entradas.html', {
        'proximas': proximas,
        'pasadas': pasadas,
        'proximo': proximo,
    })