from django.db import models
from django.contrib.auth.decorators import login_required

@login_required
def crear_reserva(request, cancha_id):
    ...

class Estadio(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='estadios/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.ciudad}"

    class Meta:
        verbose_name_plural = "Estadios"
        ordering = ['pais', 'ciudad']


class Cancha(models.Model):
    TIPO_CHOICES = [
        ('principal', 'Principal'),
        ('entrenamiento', 'Entrenamiento'),
        ('calentamiento', 'Calentamiento'),
    ]
    SUPERFICIE_CHOICES = [
        ('cesped_natural', 'Césped Natural'),
        ('cesped_sintetico', 'Césped Sintético'),
        ('tierra', 'Tierra'),
    ]
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('ocupada', 'Ocupada'),
        ('mantenimiento', 'En Mantenimiento'),
    ]

    estadio = models.ForeignKey(Estadio, on_delete=models.CASCADE, related_name='canchas')
    numero = models.PositiveIntegerField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='principal')
    superficie = models.CharField(max_length=20, choices=SUPERFICIE_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    largo = models.DecimalField(max_digits=5, decimal_places=2, help_text="En metros")
    ancho = models.DecimalField(max_digits=5, decimal_places=2, help_text="En metros")

    def __str__(self):
        return f"Cancha {self.numero} - {self.estadio.nombre}"

    class Meta:
        unique_together = ('estadio', 'numero')
        ordering = ['estadio', 'numero']


class Equipo(models.Model):
    GRUPO_CHOICES = [(f'Grupo {letra}', f'Grupo {letra}')
                     for letra in 'ABCDEFGHIJKLMNOP']  # 16 grupos para 48 equipos

    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    codigo_fifa = models.CharField(max_length=3, unique=True)  # ej: ARG, BRA
    grupo = models.CharField(max_length=10, choices=GRUPO_CHOICES)
    entrenador = models.CharField(max_length=100)
    bandera = models.ImageField(upload_to='banderas/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo_fifa})"

    class Meta:
        ordering = ['grupo', 'nombre']


class Jugador(models.Model):
    POSICION_CHOICES = [
        ('POR', 'Portero'),
        ('DEF', 'Defensa'),
        ('MED', 'Mediocampista'),
        ('DEL', 'Delantero'),
    ]

    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='jugadores')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    numero_camiseta = models.PositiveIntegerField()
    posicion = models.CharField(max_length=3, choices=POSICION_CHOICES)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return f"#{self.numero_camiseta} {self.apellido}, {self.nombre}"

    class Meta:
        unique_together = ('equipo', 'numero_camiseta')
        ordering = ['equipo', 'numero_camiseta']


class Partido(models.Model):
    FASE_CHOICES = [
        ('grupos', 'Fase de Grupos'),
        ('octavos', 'Octavos de Final'),
        ('cuartos', 'Cuartos de Final'),
        ('semifinal', 'Semifinal'),
        ('tercer_puesto', 'Tercer Puesto'),
        ('final', 'Final'),
    ]

    cancha = models.ForeignKey(Cancha, on_delete=models.PROTECT, related_name='partidos')
    equipo_local = models.ForeignKey(Equipo, on_delete=models.PROTECT, related_name='partidos_local')
    equipo_visitante = models.ForeignKey(Equipo, on_delete=models.PROTECT, related_name='partidos_visitante')
    fecha = models.DateTimeField()
    fase = models.CharField(max_length=20, choices=FASE_CHOICES)
    arbitro = models.CharField(max_length=100, blank=True)
    goles_local = models.PositiveIntegerField(null=True, blank=True)
    goles_visitante = models.PositiveIntegerField(null=True, blank=True)

    def resultado(self):
        if self.goles_local is not None and self.goles_visitante is not None:
            return f"{self.goles_local} - {self.goles_visitante}"
        return "Por jugarse"

    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante} ({self.fecha.strftime('%d/%m/%Y')})"

    class Meta:
        ordering = ['fecha']


class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE, related_name='reservas')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='reservas')
    fecha_inicio = models.DateTimeField()
    duracion_horas = models.PositiveIntegerField(default=2)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    motivo = models.TextField(blank=True, help_text="Ej: Entrenamiento pre-partido")
    creada_en = models.DateTimeField(auto_now_add=True)

# En models.py dentro de Reserva+
def clean(self):
    from django.core.exceptions import ValidationError
    conflicto = reserva.objects.filter(
        cancha=self.cancha,
        fecha_inicio=self.fecha_inicio,
        estado='confirmada'
    ).exists()
    if conflicto:
        raise ValidationError('La cancha ya está reservada en ese horario.')

    def __str__(self):
        return f"Reserva: {self.equipo} en {self.cancha} - {self.fecha_inicio.strftime('%d/%m/%Y %H:%M')}"

def editar_cancha(request, pk):
    cancha = get_object_or_404(Cancha, pk=pk)
    form = CanchaForm(request.POST or None, instance=cancha)
    if form.is_valid():
        form.save()
        return redirect('lista_canchas')
    return render(request, 'Api/editar_cancha.html', {'form': form})

def eliminar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        reserva.delete()
        return redirect('lista_canchas')
    return render(request, 'Api/confirmar_eliminar.html', {'reserva': reserva})



    class Meta:
        ordering = ['-creada_en']