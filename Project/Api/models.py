from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
import uuid


class Estadio(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='estadios/', blank=True, null=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.ciudad}"

    class Meta:
        verbose_name_plural = "Estadios"
        ordering = ['pais', 'ciudad']


class Equipo(models.Model):
    GRUPO_CHOICES = [(f'Grupo {letra}', f'Grupo {letra}')
                     for letra in 'ABCDEFGHIJKLMNOP']

    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    codigo_fifa = models.CharField(max_length=3, unique=True)
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

    estadio = models.ForeignKey(Estadio, on_delete=models.PROTECT, related_name='partidos')
    equipo_local = models.ForeignKey(Equipo, on_delete=models.PROTECT,
                                     related_name='partidos_local', null=True, blank=True)
    equipo_visitante = models.ForeignKey(Equipo, on_delete=models.PROTECT,
                                         related_name='partidos_visitante', null=True, blank=True)
    descripcion = models.CharField(max_length=200, blank=True,
                                   help_text="Ej: Ganador Grupo A vs Segundo Grupo B")
    fecha = models.DateTimeField()
    fase = models.CharField(max_length=20, choices=FASE_CHOICES)
    arbitro = models.CharField(max_length=100, blank=True)
    goles_local = models.PositiveIntegerField(null=True, blank=True)
    goles_visitante = models.PositiveIntegerField(null=True, blank=True)
    precio_general = models.DecimalField(max_digits=8, decimal_places=2, default=50.00)
    precio_platea = models.DecimalField(max_digits=8, decimal_places=2, default=150.00)
    precio_vip = models.DecimalField(max_digits=8, decimal_places=2, default=300.00)
    entradas_disponibles = models.PositiveIntegerField(default=5000)

    def resultado(self):
        if self.goles_local is not None and self.goles_visitante is not None:
            return f"{self.goles_local} - {self.goles_visitante}"
        return "Por jugarse"

    def nombre_partido(self):
        if self.equipo_local and self.equipo_visitante:
            return f"{self.equipo_local.nombre} vs {self.equipo_visitante.nombre}"
        return self.descripcion or "Partido por definir"

    def ya_jugado(self):
        return self.fecha < timezone.now()

    def dias_restantes(self):
        if self.ya_jugado():
            return 0
        delta = self.fecha - timezone.now()
        return delta.days

    def clean(self):
        conflicto = Partido.objects.filter(
            estadio=self.estadio,
            fecha=self.fecha,
        ).exclude(pk=self.pk)
        if conflicto.exists():
            raise ValidationError('Ya hay un partido programado en ese estadio a esa hora.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_partido()} ({self.fecha.strftime('%d/%m/%Y')})"

    class Meta:
        ordering = ['fecha']


class Entrada(models.Model):
    CATEGORIA_CHOICES = [
        ('general', 'General'),
        ('platea', 'Platea'),
        ('vip', 'VIP'),
    ]
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    partido = models.ForeignKey(Partido, on_delete=models.PROTECT, related_name='entradas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entradas')
    categoria = models.CharField(max_length=10, choices=CATEGORIA_CHOICES, default='general')
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='confirmada')
    fecha_compra = models.DateTimeField(auto_now_add=True)
    codigo = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.precio_total = self.precio_unitario * self.cantidad
        if not self.codigo:
            self.codigo = f"WRC26-{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo} - {self.usuario.username} - {self.partido}"

    class Meta:
        ordering = ['-fecha_compra']
        verbose_name_plural = "Entradas"


class Perfil(models.Model):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('operador', 'Operador'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='operador')

    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"

    class Meta:
        verbose_name_plural = "Perfiles"