# ⚽ WRC26 — Sistema de Gestión de Entradas
### FIFA World Cup 2026 — Canada · Mexico · USA

---

## 👥 Integrantes

| Nombre | Área |
|--------|------|
| Gustavo Estevez | Backend |
| Martin Clemente | Frontend |
| Thiago Hernandez | Documentación y Marketing |

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso |
|-----------|-----|
| Python 3.14 | Lenguaje backend |
| Django 6.0 | Framework web |
| SQLite | Base de datos |
| HTML5 / CSS3 | Frontend |
| JavaScript | Interactividad y validaciones |
| Leaflet.js | Mapas y geolocalización |

---

## 📁 Estructura de carpetas

```
WRC26/
└── Project/
    ├── manage.py
    ├── db.sqlite3
    ├── Project/
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── Api/
        ├── models.py          ← Base de datos
        ├── views.py           ← Lógica de negocio
        ├── urls.py            ← Rutas
        ├── forms.py           ← Formularios
        ├── admin.py           ← Panel de administración
        ├── tests.py           ← Tests automáticos
        ├── fixtures/
        │   ├── equipos.json   ← 48 equipos del mundial
        │   ├── estadios.json  ← 16 estadios sede
        │   └── partidos.json  ← 40 partidos del torneo
        └── Templates/
            └── canchas/
                ├── base.html
                ├── login.html
                ├── registro.html
                ├── inicio.html
                ├── lista_estadios.html
                ├── form_estadio.html
                ├── lista_partidos.html
                ├── detalle_partido.html
                ├── form_partido.html
                ├── lista_equipos.html
                ├── form_equipo.html
                ├── mapa_estadios.html
                ├── carrito.html
                ├── pago.html
                ├── compra_exitosa.html
                ├── mis_entradas.html
                ├── confirmar_eliminar.html
                ├── 403.html
                └── index.html
```

---

## 🚀 Cómo ejecutar el proyecto

### 1. Clonar el repositorio
```bash
git clone https://github.com/GustavoEstevez/WRC26.git
cd WRC26/Project
```

### 2. Instalar dependencias
```bash
pip install django
```

### 3. Aplicar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Cargar datos iniciales
```bash
python manage.py loaddata equipos.json
python manage.py loaddata estadios.json
python manage.py loaddata partidos.json
```

### 5. Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor
```bash
python manage.py runserver
```

### 7. Abrir en el navegador
```
http://127.0.0.1:8000/
```

---

## 🔐 Datos de acceso

| Rol | Usuario | Contraseña |
|-----|---------|------------|
| Administrador | admin | admin |
| Operador | usuario | usuario |

> Para cambiar el rol de un usuario: entrar al panel `/admin/` → Perfiles → cambiar rol a Administrador.

---

## ✅ Funcionalidades

**Gestión (solo Administrador)**
- Alta, baja y modificación de estadios
- Alta, baja y modificación de equipos
- Alta, baja y modificación de partidos

**Usuarios (Administrador y Operador)**
- Registro e inicio de sesión
- Ver estadios con mapa interactivo
- Ver equipos participantes del mundial
- Ver partidos por fase
- Comprar entradas con carrito de compras
- Múltiples métodos de pago (tarjeta, débito, transferencia)
- Ver mis entradas con cuenta regresiva

---

## 🗺️ Geolocalización

El sistema incorpora un mapa interactivo con los 16 estadios sede del mundial, implementado con Leaflet.js y OpenStreetMap. Cada estadio muestra su nombre, ciudad y capacidad al hacer clic en el marcador.
